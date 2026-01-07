from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .base import BaseNoteTest


class TestNotesCreation(BaseNoteTest):

    def create_note_and_assert_one(self, form_data):
        notes_before = set(Note.objects.all())
        self.author_client.post(self.ADD_URL, data=form_data)
        notes_after = set(Note.objects.all())
        self.assertEqual(len(notes_after - notes_before), 1)
        new_note = (notes_after - notes_before).pop()
        return new_note

    def test_user_can_create_note(self):
        new_note = self.create_note_and_assert_one(self.form_data)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        notes_before = set(Note.objects.all())
        response = self.client.post(self.ADD_URL, data=self.form_data)
        self.assertRedirects(response, self.REDIRECT_ADD)
        self.assertEqual(notes_before, set(Note.objects.all()))

    def test_not_unique_slug(self):
        # form_data = self.form_data.copy()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(self.ADD_URL, data=self.form_data)
        self.assertFormError(response.context['form'], 'slug',
                             errors=(self.note.slug + WARNING))
        self.assertEqual(set(Note.objects.all()), {self.note})

    def test_empty_slug(self):
        # form_data = self.form_data.copy()
        self.form_data.pop('slug')
        new_note = self.create_note_and_assert_one(self.form_data)
        self.assertEqual(new_note.slug, slugify(self.form_data['title']))
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.author)

    def test_author_can_edit_note(self):
        # form_data = self.form_data.copy()
        self.author_client.post(self.EDIT_URL, data=self.form_data)
        edited = Note.objects.get(id=self.note.id)
        self.assertEqual(edited.title, self.form_data['title'])
        self.assertEqual(edited.text, self.form_data['text'])
        self.assertEqual(edited.slug, self.form_data['slug'])
        self.assertEqual(edited.author, self.note.author)

    def test_other_user_cant_edit_note(self):
        response = self.reader_client.post(self.EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(note_from_db.title, self.note.title)
        self.assertEqual(note_from_db.text, self.note.text)
        self.assertEqual(note_from_db.slug, self.note.slug)
        self.assertEqual(note_from_db.author, self.note.author)

    def test_not_author_can_delete_note(self):
        notes_before = set(Note.objects.all())
        response = self.reader_client.post(self.DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(notes_before, set(Note.objects.all()))
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
