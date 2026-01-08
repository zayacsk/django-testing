from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .base import BaseNoteTest


class TestNotesCreation(BaseNoteTest):

    def create_note_and_assert_one(self, expected_slug):
        notes_before = set(Note.objects.all())
        response = self.author_client.post(self.ADD_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        notes_after = set(Note.objects.all())
        new_notes = notes_after - notes_before
        self.assertEqual(len(new_notes), 1)
        new_note = new_notes.pop()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.author, self.author)

    def test_user_can_create_note(self):
        self.create_note_and_assert_one(
            expected_slug=self.form_data['slug']
        )

    def test_anonymous_user_cannot_create_note(self):
        notes_before = set(Note.objects.all())
        response = self.client.post(self.ADD_URL, data=self.form_data)
        self.assertRedirects(response, self.REDIRECT_ADD)
        self.assertSetEqual(notes_before, set(Note.objects.all()))

    def test_cannot_create_note_with_existing_slug(self):
        self.form_data['slug'] = self.note.slug
        notes_before = set(Note.objects.all())
        response = self.author_client.post(self.ADD_URL, data=self.form_data)
        self.assertFormError(
            response.context['form'],
            'slug',
            errors=(self.note.slug + WARNING),
        )
        notes_after = set(Note.objects.all())
        self.assertSetEqual(notes_before, notes_after)

    def test_slug_is_generated_from_title_if_empty(self):
        self.form_data.pop('slug')
        self.create_note_and_assert_one(
            expected_slug=slugify(self.form_data['title'])
        )

    def test_author_can_edit_note(self):
        self.author_client.post(self.EDIT_URL, data=self.form_data)
        edited = Note.objects.get(id=self.note.id)
        self.assertEqual(edited.title, self.form_data['title'])
        self.assertEqual(edited.text, self.form_data['text'])
        self.assertEqual(edited.slug, self.form_data['slug'])
        self.assertEqual(edited.author, self.note.author)

    def test_reader_cannot_edit_author_note(self):
        response = self.reader_client.post(self.EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(note_from_db.title, self.note.title)
        self.assertEqual(note_from_db.text, self.note.text)
        self.assertEqual(note_from_db.slug, self.note.slug)
        self.assertEqual(note_from_db.author, self.note.author)

    def test_reader_cannot_delete_author_note(self):
        notes_before = set(Note.objects.all())
        response = self.reader_client.post(self.DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_after = set(Note.objects.all())
        self.assertSetEqual(notes_before, notes_after)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(note_from_db.title, self.note.title)
        self.assertEqual(note_from_db.text, self.note.text)
        self.assertEqual(note_from_db.slug, self.note.slug)
        self.assertEqual(note_from_db.author, self.note.author)
