from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class BaseNoteTest(TestCase):
    NOTE_SLUG = 'slug'

    OK = HTTPStatus.OK
    NOT_FOUND = HTTPStatus.NOT_FOUND
    REDIRECT = HTTPStatus.FOUND

    HOME_URL = reverse('notes:home')
    LOGIN_URL = reverse('users:login')
    LOGOUT_URL = reverse('users:logout')
    SIGNUP_URL = reverse('users:signup')
    LIST_URL = reverse('notes:list')
    ADD_URL = reverse('notes:add')
    SUCCESS_URL = reverse('notes:success')

    DETAIL_URL = reverse('notes:detail', args=(NOTE_SLUG,))
    EDIT_URL = reverse('notes:edit', args=(NOTE_SLUG,))
    DELETE_URL = reverse('notes:delete', args=(NOTE_SLUG,))

    REDIRECT_DETAIL = f'{LOGIN_URL}?next={DETAIL_URL}'
    REDIRECT_EDIT = f'{LOGIN_URL}?next={EDIT_URL}'
    REDIRECT_DELETE = f'{LOGIN_URL}?next={DELETE_URL}'
    REDIRECT_ADD = f'{LOGIN_URL}?next={ADD_URL}'
    REDIRECT_SUCCESS = f'{LOGIN_URL}?next={SUCCESS_URL}'
    REDIRECT_LIST = f'{LOGIN_URL}?next={LIST_URL}'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.reader = User.objects.create(username='Reader')
        cls.note = Note.objects.create(
            title='Title',
            text='Text',
            slug=cls.NOTE_SLUG,
            author=cls.author
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.form_data = {
            'title': 'New title',
            'text': 'New text',
            'slug': 'new-slug',
        }
