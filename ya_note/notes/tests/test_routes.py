from .base import BaseNoteTest
from . import urls


class TestRoutes(BaseNoteTest):

    def test_pages_status_codes(self):
        cases = (
            (urls.HOME_URL, self.client, self.OK),
            (urls.LOGIN_URL, self.client, self.OK),
            (urls.SIGNUP_URL, self.client, self.OK),

            (urls.LIST_URL, self.author_client, self.OK),
            (urls.ADD_URL, self.author_client, self.OK),
            (urls.SUCCESS_URL, self.author_client, self.OK),
            (urls.DETAIL_URL, self.author_client, self.OK),
            (urls.EDIT_URL, self.author_client, self.OK),
            (urls.DELETE_URL, self.author_client, self.OK),

            (urls.DETAIL_URL, self.reader_client, self.NOT_FOUND),
            (urls.EDIT_URL, self.reader_client, self.NOT_FOUND),
            (urls.DELETE_URL, self.reader_client, self.NOT_FOUND),
        )

        for url, client, status in cases:
            with self.subTest(url=url, status=status):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirects_for_anonymous_user(self):
        for url, expected_url in self.redirect_cases:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    expected_url
                )
