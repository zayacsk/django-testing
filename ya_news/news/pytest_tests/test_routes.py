import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('news_id_for_args')),
        ('users:login', None),
        ('users:signup', None),
        ('users:logout', None),
    ),
)
def test_pages_availability(client, name, args):
    url = reverse(name, args=(args))
    response = (
        client.post(url)
        if name == 'users:logout'
        else client.get(url)
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'user, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
    ),
)
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('comment_id_for_args')),
    ),
)
def test_availability_for_comment_edit_and_delete(expected_status, user,
                                                  name, args):
    url = reverse(name, args=(args))
    response = user.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        'news:edit',
        'news:delete',
    ),
)
def test_redirect_for_anonymous_client(comment_id_for_args,
                                       client, name):
    login_url = reverse('users:login')
    url = reverse(name, args=comment_id_for_args)
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
