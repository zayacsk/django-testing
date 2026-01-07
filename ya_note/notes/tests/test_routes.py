from .base import BaseNoteTest


class TestRoutes(BaseNoteTest):

    def test_pages_status_codes(self):
        cases = (
            (self.HOME_URL, self.client, self.OK),
            (self.LOGIN_URL, self.client, self.OK),
            (self.SIGNUP_URL, self.client, self.OK),

            (self.LIST_URL, self.author_client, self.OK),
            (self.ADD_URL, self.author_client, self.OK),
            (self.SUCCESS_URL, self.author_client, self.OK),
            (self.DETAIL_URL, self.author_client, self.OK),
            (self.EDIT_URL, self.author_client, self.OK),
            (self.DELETE_URL, self.author_client, self.OK),

            (self.DETAIL_URL, self.reader_client, self.NOT_FOUND),
            (self.EDIT_URL, self.reader_client, self.NOT_FOUND),
            (self.DELETE_URL, self.reader_client, self.NOT_FOUND),
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
