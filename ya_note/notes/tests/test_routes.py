from .base import BaseNoteTest


class TestRoutes(BaseNoteTest):

    def test_pages_status_codes(self):
        cases = (
            (self.LIST_URL, self.author_client, self.OK),
            (self.ADD_URL, self.author_client, self.OK),
            (self.SUCCESS_URL, self.author_client, self.OK),
            (self.DETAIL_URL, self.author_client, self.OK),
            (self.EDIT_URL, self.author_client, self.OK),
            (self.DELETE_URL, self.author_client, self.OK),

            (self.DETAIL_URL, self.reader_client, self.NOT_FOUND),
            (self.EDIT_URL, self.reader_client, self.NOT_FOUND),
            (self.DELETE_URL, self.reader_client, self.NOT_FOUND),

            (self.HOME_URL, self.client, self.OK),
            (self.LOGIN_URL, self.client, self.OK),
            (self.SIGNUP_URL, self.client, self.OK),
            (self.LIST_URL, self.client, self.REDIRECT),
            (self.ADD_URL, self.client, self.REDIRECT),
            (self.SUCCESS_URL, self.client, self.REDIRECT),
            (self.DETAIL_URL, self.client, self.REDIRECT),
            (self.EDIT_URL, self.client, self.REDIRECT),
            (self.DELETE_URL, self.client, self.REDIRECT),
        )

        for url, client, status in cases:
            with self.subTest(url=url, status=status):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirects_for_anonymous_user(self):
        redirect_cases = (
            (self.DETAIL_URL, f'{self.LOGIN_URL}?next={self.DETAIL_URL}'),
            (self.EDIT_URL, f'{self.LOGIN_URL}?next={self.EDIT_URL}'),
            (self.DELETE_URL, f'{self.LOGIN_URL}?next={self.DELETE_URL}'),
            (self.ADD_URL, f'{self.LOGIN_URL}?next={self.ADD_URL}'),
            (self.SUCCESS_URL, f'{self.LOGIN_URL}?next={self.SUCCESS_URL}'),
            (self.LIST_URL, f'{self.LOGIN_URL}?next={self.LIST_URL}'),
        )
        for url, expected_url in redirect_cases:
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), expected_url)
