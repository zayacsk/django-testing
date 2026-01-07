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

        cls.HOME_URL = reverse('notes:home')
        cls.LOGIN_URL = reverse('users:login')
        cls.LOGOUT_URL = reverse('users:logout')
        cls.SIGNUP_URL = reverse('users:signup')
        cls.LIST_URL = reverse('notes:list')
        cls.ADD_URL = reverse('notes:add')
        cls.SUCCESS_URL = reverse('notes:success')

        cls.DETAIL_URL = reverse('notes:detail', args=(cls.NOTE_SLUG,))
        cls.EDIT_URL = reverse('notes:edit', args=(cls.NOTE_SLUG,))
        cls.DELETE_URL = reverse('notes:delete', args=(cls.NOTE_SLUG,))

        cls.REDIRECT_DETAIL = f'{cls.LOGIN_URL}?next={cls.DETAIL_URL}'
        cls.REDIRECT_EDIT = f'{cls.LOGIN_URL}?next={cls.EDIT_URL}'
        cls.REDIRECT_DELETE = f'{cls.LOGIN_URL}?next={cls.DELETE_URL}'
        cls.REDIRECT_ADD = f'{cls.LOGIN_URL}?next={cls.ADD_URL}'
        cls.REDIRECT_SUCCESS = f'{cls.LOGIN_URL}?next={cls.SUCCESS_URL}'
        cls.REDIRECT_LIST = f'{cls.LOGIN_URL}?next={cls.LIST_URL}'
