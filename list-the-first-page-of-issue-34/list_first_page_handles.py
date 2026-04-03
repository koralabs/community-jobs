#!/usr/bin/env python3
"""Fetch the first paginated JSON page of Handles from api.handle.me."""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

API_BASE_URL = "https://api.handle.me"
DEFAULT_PAGE = 1
DEFAULT_RECORDS_PER_PAGE = 100
MAX_RECORDS_PER_PAGE = 250
REQUEST_TIMEOUT_SECONDS = 30
MAX_REQUESTS_PER_SECOND_PER_HOST = 5
MIN_SECONDS_BETWEEN_REQUESTS = 1 / MAX_REQUESTS_PER_SECOND_PER_HOST
KORA_USER_AGENT_ENV_VAR = "KORA_USER_AGENT"
DEFAULT_ENV_FILE = Path.home() / "src" / "koralabs" / ".env"


class PerHostRateLimiter:
    """Enforce the executor's 5 requests/second/host ceiling."""

    def __init__(self, min_seconds_between_requests: float = MIN_SECONDS_BETWEEN_REQUESTS) -> None:
        self._min_seconds_between_requests = min_seconds_between_requests
        self._last_request_started_by_host: dict[str, float] = {}

    def wait(self, host: str) -> None:
        previous_request_started = self._last_request_started_by_host.get(host)
        if previous_request_started is not None:
            elapsed = time.monotonic() - previous_request_started
            if elapsed < self._min_seconds_between_requests:
                time.sleep(self._min_seconds_between_requests - elapsed)

        self._last_request_started_by_host[host] = time.monotonic()


def read_env_file(env_file: Path) -> dict[str, str]:
    values: dict[str, str] = {}

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()

        key, separator, value = line.partition("=")
        if not separator:
            continue

        normalized_key = key.strip()
        if not normalized_key:
            continue

        normalized_value = value.strip()
        if normalized_value[:1] == normalized_value[-1:] and normalized_value[:1] in {"'", '"'}:
            normalized_value = normalized_value[1:-1]

        values[normalized_key] = normalized_value

    return values


def load_kora_user_agent(env_file: Path | None) -> str:
    env_value = os.environ.get(KORA_USER_AGENT_ENV_VAR, "").strip()
    if env_value:
        return env_value

    if env_file is None:
        raise RuntimeError(
            f"{KORA_USER_AGENT_ENV_VAR} must be set in the environment or provided via --env-file"
        )

    if not env_file.is_file():
        raise RuntimeError(
            f"{KORA_USER_AGENT_ENV_VAR} was not set and env file was not found at {env_file}"
        )

    env_values = read_env_file(env_file)
    file_value = env_values.get(KORA_USER_AGENT_ENV_VAR, "").strip()
    if not file_value:
        raise RuntimeError(f"{KORA_USER_AGENT_ENV_VAR} was not found in {env_file}")

    return file_value


def build_handles_url(base_url: str, page: int, records_per_page: int) -> str:
    if page < 1:
        raise ValueError("page must be >= 1")
    if not 1 <= records_per_page <= MAX_RECORDS_PER_PAGE:
        raise ValueError(f"records_per_page must be between 1 and {MAX_RECORDS_PER_PAGE}")

    handles_url = urljoin(base_url.rstrip("/") + "/", "handles")
    query_string = urlencode(
        {
            "page": page,
            "records_per_page": records_per_page,
        }
    )
    return f"{handles_url}?{query_string}"


def fetch_handles_page(
    *,
    page: int = DEFAULT_PAGE,
    records_per_page: int = DEFAULT_RECORDS_PER_PAGE,
    base_url: str = API_BASE_URL,
    user_agent: str,
    timeout_seconds: int = REQUEST_TIMEOUT_SECONDS,
    rate_limiter: PerHostRateLimiter | None = None,
) -> dict[str, Any]:
    if not user_agent.strip():
        raise ValueError("user_agent is required")

    handles_url = build_handles_url(base_url=base_url, page=page, records_per_page=records_per_page)
    parsed_url = urlparse(handles_url)

    if rate_limiter is not None:
        rate_limiter.wait(parsed_url.netloc)

    request = Request(
        handles_url,
        headers={
            "Accept": "application/json",
            "User-Agent": user_agent,
        },
    )

    with urlopen(request, timeout=timeout_seconds) as response:
        total_header = response.headers.get("x-handles-search-total")
        if total_header is None:
            raise RuntimeError("Response missing x-handles-search-total header")

        try:
            total_matching_handles = int(total_header)
        except ValueError as exc:
            raise RuntimeError("x-handles-search-total header must be an integer") from exc

        payload = json.load(response)
        status_code = getattr(response, "status", response.getcode())

    if not isinstance(payload, list):
        raise ValueError("Expected the /handles JSON response body to be a list")

    handle_names: list[str] = []
    for index, handle in enumerate(payload):
        if not isinstance(handle, dict):
            raise ValueError(f"Handle at index {index} is not an object")

        handle_name = handle.get("name")
        if not isinstance(handle_name, str):
            raise ValueError(f"Handle at index {index} is missing a string 'name' field")

        handle_names.append(handle_name)

    is_up_to_date = status_code == 200
    if status_code == 200:
        status_description = "successful_and_up_to_date"
    elif status_code == 202:
        status_description = "successful_but_scanner_still_catching_up"
    else:
        status_description = "unexpected_status_code"

    return {
        "captured_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "request": {
            "url": handles_url,
            "page": page,
            "records_per_page": records_per_page,
            "accept": "application/json",
        },
        "summary": {
            "status_code": status_code,
            "status_description": status_description,
            "is_up_to_date": is_up_to_date,
            "returned_count": len(handle_names),
            "total_matching_handles": total_matching_handles,
            "first_handle_name": handle_names[0] if handle_names else "",
            "last_handle_name": handle_names[-1] if handle_names else "",
        },
        "handle_names": handle_names,
    }


def write_output(result: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    default_output_path = Path(__file__).with_name("output.json")

    parser = argparse.ArgumentParser(
        description="Fetch the first page of handles from https://api.handle.me/handles and save a JSON artifact."
    )
    parser.add_argument("--page", type=int, default=DEFAULT_PAGE, help="Page number to fetch. Defaults to 1.")
    parser.add_argument(
        "--records-per-page",
        type=int,
        default=DEFAULT_RECORDS_PER_PAGE,
        help="Page size to request. Defaults to 100, maximum 250.",
    )
    parser.add_argument(
        "--base-url",
        default=API_BASE_URL,
        help="Base API URL. Defaults to https://api.handle.me.",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=DEFAULT_ENV_FILE,
        help=(
            "Path to a .env file that defines KORA_USER_AGENT. "
            f"Defaults to {DEFAULT_ENV_FILE}."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output_path,
        help=f"Path for the JSON output artifact. Defaults to {default_output_path}.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    user_agent = load_kora_user_agent(args.env_file)
    result = fetch_handles_page(
        page=args.page,
        records_per_page=args.records_per_page,
        base_url=args.base_url,
        user_agent=user_agent,
        rate_limiter=PerHostRateLimiter(),
    )
    write_output(result, args.output)

    print(f"Wrote {result['summary']['returned_count']} handles to {args.output}")
    print(f"Total matching handles reported by API: {result['summary']['total_matching_handles']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
