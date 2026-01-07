from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

from .base import BaseNoteTest
from . import urls


class TestNotesCreation(BaseNoteTest):

    def test_user_can_create_note(self):
        notes_before = set(Note.objects.all())
        form_data = self.FORM_DATA.copy()
        self.author_client.post(urls.ADD_URL, data=form_data)
        new_note = (set(Note.objects.all()) - notes_before).pop()
        self.assertEqual(new_note.title, form_data['title'])
        self.assertEqual(new_note.text, form_data['text'])
        self.assertEqual(new_note.slug, form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        notes_before = set(Note.objects.all())
        response = self.anonymous_client.post(
            urls.ADD_URL,
            data={'title': 'X', 'text': 'Y'}
        )
        self.assertRedirects(
            response,
            f'{urls.LOGIN_URL}?next={urls.ADD_URL}'
        )
        self.assertEqual(notes_before, set(Note.objects.all()))

    def test_not_unique_slug(self):
        notes_before = set(Note.objects.all())
        form_data = self.FORM_DATA.copy()
        form_data['slug'] = self.note.slug
        response = self.author_client.post(urls.ADD_URL, data=form_data)
        self.assertFormError(
            response.context['form'],
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(notes_before, set(Note.objects.all()))

    def test_empty_slug(self):
        notes_before = set(Note.objects.all())
        form_data = self.FORM_DATA.copy()
        form_data.pop('slug')
        self.author_client.post(urls.ADD_URL, data=form_data)
        new_note = (set(Note.objects.all()) - notes_before).pop()
        self.assertEqual(new_note.slug, slugify(form_data['title']))
        self.assertEqual(new_note.title, form_data['title'])
        self.assertEqual(new_note.text, form_data['text'])
        self.assertEqual(new_note.author, self.author)

    def test_author_can_edit_note(self):
        form_data = self.FORM_DATA.copy()
        self.author_client.post(urls.EDIT_URL, data=form_data)
        edited = Note.objects.get(id=self.note.id)
        self.assertEqual(edited.title, form_data['title'])
        self.assertEqual(edited.text, form_data['text'])
        self.assertEqual(edited.slug, form_data['slug'])
        self.assertEqual(edited.author, self.author)

    def test_other_user_cant_edit_note(self):
        form_data = {
            'title': 'Hack',
            'text': 'Hack',
            'slug': urls.NEW_SLUG,
        }
        response = self.reader_client.post(urls.EDIT_URL, data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_other_user_cant_edit_note(self):
        notes_before = set(Note.objects.all())
        form_data = self.FORM_DATA.copy()
        response = self.reader_client.post(urls.EDIT_URL, data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(notes_before, set(Note.objects.all()))
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(note_from_db.title, self.note.title)
        self.assertEqual(note_from_db.text, self.note.text)
        self.assertEqual(note_from_db.slug, self.note.slug)
        self.assertEqual(note_from_db.author, self.note.author)

    def test_not_author_can_delete_note(self):
        notes_before = set(Note.objects.all())
        response = self.reader_client.post(urls.DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(notes_before, set(Note.objects.all()))
