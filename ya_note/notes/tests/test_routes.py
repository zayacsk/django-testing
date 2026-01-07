from http import HTTPStatus

from .base import BaseNoteTest
from . import urls


class TestRoutes(BaseNoteTest):

    def test_pages_status_codes(self):
        cases = [
            (urls.HOME_URL, self.anonymous_client, HTTPStatus.OK),
            (urls.LOGIN_URL, self.anonymous_client, HTTPStatus.OK),
            (urls.SIGNUP_URL, self.anonymous_client, HTTPStatus.OK),
            (urls.LIST_URL, self.author_client, HTTPStatus.OK),
            (urls.ADD_URL, self.author_client, HTTPStatus.OK),
            (urls.SUCCESS_URL, self.author_client, HTTPStatus.OK),
            (urls.DETAIL_URL, self.author_client, HTTPStatus.OK),
            (urls.EDIT_URL, self.author_client, HTTPStatus.OK),
            (urls.DELETE_URL, self.author_client, HTTPStatus.OK),
            (urls.DETAIL_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (urls.EDIT_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (urls.DELETE_URL, self.reader_client, HTTPStatus.NOT_FOUND),
        ]
        for url, client, status in cases:
            with self.subTest(url=url, status=status):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirects_for_anonymous_user(self):
        protected_urls = (
            urls.DETAIL_URL,
            urls.EDIT_URL,
            urls.DELETE_URL,
            urls.ADD_URL,
            urls.SUCCESS_URL,
            urls.LIST_URL,
        )
        for url in protected_urls:
            with self.subTest(url=url):
                expected_url = f'{urls.LOGIN_URL}?next={url}'
                self.assertRedirects(
                    self.anonymous_client.get(url),
                    expected_url
                )
