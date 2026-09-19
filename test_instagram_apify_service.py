from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import Mock, patch

import requests

from app.services import instagram_apify_service as service


class InstagramApifyTests(unittest.TestCase):
    def setUp(self):
        token = patch.object(service, "APIFY_TOKEN", "token-ficticio")
        token.start()
        self.addCleanup(token.stop)
        http = patch.object(service.requests, "post")
        self.http = http.start()
        self.addCleanup(http.stop)
        self.url = "https://www.instagram.com/exemplo/"
        self.profile = {"username": "exemplo", "followersCount": 3000, "postsCount": 80}
        self.posts = [{
            "timestamp": "2025-10-18T23:59:45.000Z",
            "latestComments": [{"timestamp": "2025-10-20T00:00:00Z"}],
        }]

    def responses(self, profile, posts):
        self.http.side_effect = [
            Mock(json=Mock(return_value=profile)),
            Mock(json=Mock(return_value=posts)),
        ]

    def test_normal_response_and_authentication(self):
        self.responses([self.profile], self.posts)
        self.assertEqual(service.collect_instagram_data(self.url), {
            "profile": self.profile, "posts": self.posts,
        })
        calls = self.http.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertIn("apify~instagram-profile-scraper/", calls[0].args[0])
        self.assertEqual(calls[0].kwargs["json"], {"usernames": ["exemplo"]})
        self.assertIn("apify~instagram-scraper/", calls[1].args[0])
        for call in calls:
            self.assertEqual(call.kwargs["params"], {"token": "token-ficticio"})
            self.assertEqual(call.kwargs["timeout"], 300)

    def test_empty_profile(self):
        self.responses([], self.posts)
        self.assertEqual(service.collect_instagram_data(self.url), {
            "profile": None, "posts": self.posts,
        })

    def test_empty_posts(self):
        self.responses([self.profile], [])
        self.assertEqual(service.collect_instagram_data(self.url), {
            "profile": self.profile, "posts": [],
        })

    def test_http_failure(self):
        failed = Mock()
        failed.raise_for_status.side_effect = requests.HTTPError("simulado")
        self.http.return_value = failed
        self.assertEqual(service.collect_instagram_data(self.url), {
            "profile": None, "posts": [],
        })

    def test_network_failure_preserves_profile(self):
        self.http.side_effect = [
            Mock(json=Mock(return_value=[self.profile])), requests.Timeout(),
        ]
        self.assertEqual(service.collect_instagram_data(self.url), {
            "profile": self.profile, "posts": [],
        })

    def test_invalid_url(self):
        for url in [None, "", "exemplo", "https://instagram.com.evil/exemplo",
                    "https://instagram.com/p/abc/", "https://instagram.com/",
                    "https://instagram.com/accounts/", "https://[invalid"]:
            with self.subTest(url=url):
                self.assertEqual(service.collect_instagram_data(url), {
                    "profile": None, "posts": [],
                })
        self.http.assert_not_called()

    def test_three_posts_limit(self):
        self.responses([self.profile], self.posts * 5)
        result = service.collect_instagram_data(self.url)
        self.assertEqual(len(result["posts"]), 3)
        self.assertEqual(self.http.call_args.kwargs["json"], {
            "directUrls": [self.url], "resultsType": "posts", "resultsLimit": 3,
        })

    def test_private_profile_skips_posts(self):
        self.profile["private"] = True
        self.responses([self.profile], self.posts)
        self.assertEqual(service.collect_instagram_data(self.url), {
            "profile": self.profile, "posts": [],
        })
        self.assertEqual(self.http.call_count, 1)

    def test_invalid_data_and_actor_errors(self):
        for data in [None, {}, "invalid", [None, {}, {"error": "private"}]]:
            with self.subTest(data=data):
                self.responses(data, data)
                self.assertEqual(service.collect_instagram_data(self.url), {
                    "profile": None, "posts": [],
                })

    def test_invalid_json(self):
        self.http.return_value.json.side_effect = ValueError("invalid JSON")
        self.assertEqual(service.collect_instagram_data(self.url), {
            "profile": None, "posts": [],
        })

    def test_missing_token(self):
        with patch.object(service, "APIFY_TOKEN", None):
            self.assertEqual(service.collect_instagram_data(self.url), {
                "profile": None, "posts": [],
            })
        self.http.assert_not_called()

    def test_safe_diagnostics(self):
        sensitive = (
            "https://api.apify.com/?token=token-ficticio "
            "caption-secreta comentario-secreto https://media.example/private"
        )
        cases = [
            ("http_error", 401, requests.HTTPError(sensitive), None),
            ("network_error", None, requests.ConnectionError(sensitive), None),
            ("invalid_json", 200, ValueError(sensitive), None),
            ("invalid_json", 200,
             requests.exceptions.JSONDecodeError(sensitive, sensitive, 0), None),
            ("unexpected_response_format", 200, None, {"body": sensitive}),
            ("actor_item_error", 200, None, [{"error": sensitive}]),
        ]
        for category, status, error, data in cases:
            with self.subTest(category=category, error_type=type(error).__name__):
                self.http.reset_mock(return_value=True, side_effect=True)
                response = Mock(status_code=status)
                if category == "network_error":
                    self.http.side_effect = error
                else:
                    self.http.return_value = response
                    if category == "http_error":
                        response.raise_for_status.side_effect = error
                    elif category == "invalid_json":
                        response.json.side_effect = error
                    else:
                        response.json.return_value = data
                output = StringIO()
                with redirect_stdout(output):
                    result = service._run_actor(
                        "apify~instagram-scraper", {}, username="exemplo", stage="posts"
                    )
                self.assertEqual(result, [])
                suffix = f" status={status}" if status is not None else ""
                self.assertEqual(output.getvalue(), (
                    f"[Instagram Apify] actor=apify/instagram-scraper "
                    f"error={category}{suffix} username=exemplo stage=posts\n"
                    + ("[Instagram Apify] actor=apify/instagram-scraper "
                       "error=empty_result status=200 username=exemplo stage=posts\n"
                       if category == "actor_item_error" else "")
                ))
                for secret in ["token-ficticio", "https://", "caption-secreta",
                               "comentario-secreto", sensitive]:
                    self.assertNotIn(secret, output.getvalue())

    def test_actor_error_preserves_valid_items(self):
        self.http.return_value = Mock(
            status_code=200,
            json=Mock(return_value=[{"error": "token-ficticio"}, self.profile]),
        )
        output = StringIO()
        with redirect_stdout(output):
            result = service._run_actor("apify~instagram-profile-scraper", {})
        self.assertEqual(result, [self.profile])
        self.assertEqual(output.getvalue(), (
            "[Instagram Apify] actor=apify/instagram-profile-scraper "
            "error=actor_item_error status=200\n"
        ))
        self.assertNotIn("token-ficticio", output.getvalue())

    def test_stage_success_and_empty_result(self):
        self.responses([self.profile], [])
        output = StringIO()
        with redirect_stdout(output):
            service.collect_instagram_data("https://instagram.com/EXEMPLO/")
        self.assertIn("error=success username=exemplo stage=profile", output.getvalue())
        self.assertIn("error=empty_result username=exemplo stage=posts", output.getvalue())
        self.assertNotIn("token-ficticio", output.getvalue())


if __name__ == "__main__":
    unittest.main()
