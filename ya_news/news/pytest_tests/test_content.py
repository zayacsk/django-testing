import pytest

from news.forms import CommentForm
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE

pytestmark = pytest.mark.django_db


def test_news_count(client, multiple_news, home_url):
    response = client.get(home_url)
    assert response.context['news_feed'].count() == NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, multiple_news, home_url):
    response = client.get(home_url)
    news_dates = [news.date for news in response.context['news_feed']]
    assert news_dates == sorted(news_dates, reverse=True)


def test_comments_order(client, multiple_comment, detail_url):
    response = client.get(detail_url)
    timestamps = [
        comment.created
        for comment in response.context['news'].comment_set.all()
    ]
    assert timestamps == sorted(timestamps)


def test_anonymous_client_has_no_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, detail_url):
    response = author_client.get(detail_url)
    assert isinstance(response.context.get('form'), CommentForm)
