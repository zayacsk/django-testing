from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from notes.models import Note
from .urls import NOTE_SLUG, NEW_SLUG

User = get_user_model()


class BaseNoteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.reader = User.objects.create(username='Reader')
        cls.note = Note.objects.create(
            title='Title',
            text='Text',
            slug=NOTE_SLUG,
            author=cls.author
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.anonymous_client = Client()
        cls.FORM_DATA = {
            'title': 'New title',
            'text': 'New text',
            'slug': NEW_SLUG,
        }
