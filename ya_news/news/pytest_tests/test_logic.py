from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


COMMENT_DATA = {'text': 'Comment text'}

BAD_WORDS_DATA = [
    {'text': f'Текст с {bad_word}'} for bad_word in BAD_WORDS
]


def test_anonymous_user_cant_create_comment(client, detail_url):
    client.post(detail_url, data=COMMENT_DATA)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
    author_client, author, news, detail_url, detail_with_comments_url
):
    response = author_client.post(detail_url, data=COMMENT_DATA)
    assertRedirects(response, detail_with_comments_url)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_DATA['text']
    assert comment.author == author
    assert comment.news == news


@pytest.mark.parametrize('comment_data', BAD_WORDS_DATA)
def test_user_cant_use_bad_words(author_client, detail_url, comment_data):
    response = author_client.post(detail_url, data=comment_data)
    assertFormError(
        form=response.context['form'],
        field='text',
        errors=WARNING,
    )
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
    author_client, delete_url, detail_with_comments_url
):
    response = author_client.delete(delete_url)
    assertRedirects(response, detail_with_comments_url)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment, delete_url
):
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
    comment_from_db = Comment.objects.get(pk=comment.pk)
    assert comment_from_db.text == comment.text
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


def test_author_can_edit_comment(
    author_client, comment, edit_url, detail_with_comments_url
):
    response = author_client.post(edit_url, data=COMMENT_DATA)
    assertRedirects(response, detail_with_comments_url)
    assert Comment.objects.count() == 1
    edited_comment = Comment.objects.get(pk=comment.pk)
    assert edited_comment.text == COMMENT_DATA['text']
    assert edited_comment.author == comment.author
    assert edited_comment.news == comment.news


def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, edit_url
):
    response = not_author_client.post(edit_url, data=COMMENT_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
    comment_from_db = Comment.objects.get(pk=comment.pk)
    assert comment_from_db.text == comment.text
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news
