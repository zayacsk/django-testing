from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

HOME_URL = pytest.lazy_fixture('home_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')
REDIRECT_EDIT = pytest.lazy_fixture('redirect_to_login_edit')
REDIRECT_DELETE = pytest.lazy_fixture('redirect_to_login_delete')

CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')


@pytest.mark.parametrize(
    'url, client_fixture, expected_status',
    (
        (HOME_URL, CLIENT, HTTPStatus.OK),
        (DETAIL_URL, CLIENT, HTTPStatus.OK),
        (LOGIN_URL, CLIENT, HTTPStatus.OK),
        (SIGNUP_URL, CLIENT, HTTPStatus.OK),
        (LOGOUT_URL, CLIENT, HTTPStatus.OK),

        (EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (EDIT_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (DELETE_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
    ),
)
def test_pages_availability(url, client_fixture, expected_status):
    response = (client_fixture.post(url)
                if 'logout' in url
                else client_fixture.get(url))
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_redirect',
    (
        (EDIT_URL, REDIRECT_EDIT),
        (DELETE_URL, REDIRECT_DELETE),
    ),
)
def test_redirects_for_anonymous(client, url, expected_redirect):
    response = client.get(url)
    assertRedirects(response, expected_redirect)
