import json
import os
import tempfile
import threading
import unittest
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest import mock

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from list_first_page_handles import fetch_handles_page, load_kora_user_agent


class FetchHandlesPageTests(unittest.TestCase):
    @contextmanager
    def serve_response(self, *, total_header, payload, status=200):
        requests = []
        request_headers = []
        body = json.dumps(payload).encode("utf-8")

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append(self.path)
                request_headers.append(
                    {
                        "Accept": self.headers.get("Accept"),
                        "User-Agent": self.headers.get("User-Agent"),
                    }
                )
                self.send_response(status)
                if total_header is not None:
                    self.send_header("x-handles-search-total", str(total_header))
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format, *args):  # noqa: A003
                return

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            yield f"http://127.0.0.1:{server.server_port}", requests, request_headers
        finally:
            server.shutdown()
            thread.join()
            server.server_close()

    def test_fetch_handles_page_reads_names_total_header_and_user_agent(self):
        """Feature: the script returns handle names and total count while sending the required request headers.
        Failure mode: broken query construction or missing headers would return the wrong payload or violate API policy.
        Negative control: this test would fail if the request skipped the User-Agent header or omitted 'beta' from the payload.
        """

        payload = [{"name": "alpha"}, {"name": "beta"}]
        with self.serve_response(total_header=265555, payload=payload) as (base_url, requests, request_headers):
            result = fetch_handles_page(
                page=1,
                records_per_page=2,
                base_url=base_url,
                user_agent="kora-test/1.0",
            )

        self.assertEqual(result["summary"]["returned_count"], 2)
        self.assertEqual(result["summary"]["total_matching_handles"], 265555)
        self.assertEqual(result["summary"]["status_code"], 200)
        self.assertEqual(result["summary"]["status_description"], "successful_and_up_to_date")
        self.assertTrue(result["summary"]["is_up_to_date"])
        self.assertEqual(result["handle_names"], ["alpha", "beta"])
        self.assertEqual(requests, ["/handles?page=1&records_per_page=2"])
        self.assertEqual(request_headers, [{"Accept": "application/json", "User-Agent": "kora-test/1.0"}])

    def test_load_kora_user_agent_reads_quoted_export_from_env_file(self):
        """Feature: the script can load KORA_USER_AGENT from a standard exported .env entry.
        Failure mode: quoted values from the ecosystem .env file would be parsed incorrectly and break live requests.
        Negative control: this test would fail if the env file omitted KORA_USER_AGENT or left the surrounding quotes in place.
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            env_file = Path(temp_dir) / ".env"
            env_file.write_text('export KORA_USER_AGENT="kora-test/1.0"\n', encoding="utf-8")

            with mock.patch.dict(os.environ, {}, clear=True):
                user_agent = load_kora_user_agent(env_file)

        self.assertEqual(user_agent, "kora-test/1.0")

    def test_fetch_handles_page_requires_total_header(self):
        """Feature: the script rejects responses that do not include the total-count header.
        Failure mode: a missing header would silently produce an incomplete summary.
        Negative control: this test would stop failing if the helper ignored the missing header and guessed a total.
        """

        with self.serve_response(total_header=None, payload=[{"name": "alpha"}]) as (base_url, _requests, _headers):
            with self.assertRaisesRegex(RuntimeError, "x-handles-search-total"):
                fetch_handles_page(
                    page=1,
                    records_per_page=1,
                    base_url=base_url,
                    user_agent="kora-test/1.0",
                )

    def test_fetch_handles_page_requires_name_fields(self):
        """Feature: every returned handle object must expose a string name for the artifact list.
        Failure mode: malformed objects would leak into the output without an actionable error.
        Negative control: this test would fail if the payload used {'name': 'alpha'} instead of a missing field.
        """

        with self.serve_response(total_header=1, payload=[{"hex": "616c706861"}]) as (base_url, _requests, _headers):
            with self.assertRaisesRegex(ValueError, "missing a string 'name'"):
                fetch_handles_page(
                    page=1,
                    records_per_page=1,
                    base_url=base_url,
                    user_agent="kora-test/1.0",
                )


if __name__ == "__main__":
    unittest.main()
