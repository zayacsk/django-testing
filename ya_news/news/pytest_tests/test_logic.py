import pytest
from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.conftest import COMMENT_TEXT, NEW_COMMENT_TEXT


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, detail_url):
    client.post(detail_url, data={'text': COMMENT_TEXT})
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_user_can_create_comment(author_client, author, news, detail_url):
    response = author_client.post(detail_url, data={'text': COMMENT_TEXT})
    assertRedirects(response, f'{detail_url}#comments')
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.author == author
    assert comment.news == news


def test_user_cant_use_bad_words(author_client, detail_url):
    bad_words_data = {'text': f'Текст с {BAD_WORDS[0]}'}
    response = author_client.post(detail_url, data=bad_words_data)
    form = response.context['form']
    assertFormError(
        form=form,
        field='text',
        errors=WARNING
    )
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_author_can_delete_comment(author_client, detail_url, delete_url):
    url_to_comment = detail_url + '#comments'
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comment)
    assert response.status_code == HTTPStatus.FOUND
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_user_cant_delete_comment_of_another_user(not_author_client,
                                                  delete_url):
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_count = Comment.objects.count()
    assert comment_count == 1


def test_author_can_edit_comment(author_client, comment, detail_url, edit_url):
    url_to_comment = detail_url + '#comments'
    response = author_client.post(edit_url, data={'text': NEW_COMMENT_TEXT})
    assertRedirects(response, url_to_comment)
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(not_author_client,
                                                comment, edit_url):
    response = not_author_client.post(edit_url,
                                      data={'text': NEW_COMMENT_TEXT})
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT
