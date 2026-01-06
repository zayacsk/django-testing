import pytest
from datetime import timedelta

from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


COMMENT_TEXT = 'Comment text'
NEW_COMMENT_TEXT = 'New comment text'


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
    all_news = [
        News(
            title='Title',
            text='Text.',
        )
        for _ in range(11)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def news_id_for_args(news):
    return (news.id,)


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text=COMMENT_TEXT,
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
def comment_id_for_args(comment):
    return (comment.id,)


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))
