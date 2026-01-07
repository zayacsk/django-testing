from datetime import timedelta

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Reader')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Title',
        text='Text',
    )


@pytest.fixture
def multiple_news():
    for index in range(NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News.objects.create(
            title='Title',
            text='Text'
        )
        news.date = timezone.now() + timedelta(days=index)
        news.save()


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Comment text',
    )


@pytest.fixture
def multiple_comment(news, author):
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Text {index}',
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def redirect_to_login_edit(login_url, edit_url):
    return f'{login_url}?next={edit_url}'


@pytest.fixture
def redirect_to_login_delete(login_url, delete_url):
    return f'{login_url}?next={delete_url}'


@pytest.fixture
def detail_with_comments_url(detail_url):
    return f'{detail_url}#comments'
