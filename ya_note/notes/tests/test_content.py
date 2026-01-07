from notes.forms import NoteForm

from .base import BaseNoteTest
from . import urls


class TestContent(BaseNoteTest):

    def test_note_in_list_for_author(self):
        response = self.author_client.get(urls.LIST_URL)
        note = response.context['notes_feed'][0]
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_note_not_in_list_for_reader(self):
        response = self.reader_client.get(urls.LIST_URL)
        self.assertNotIn(self.note, response.context['notes_feed'])

    def test_pages_contains_form(self):
        for url in (urls.ADD_URL, urls.EDIT_URL):
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'),
                    NoteForm
                )
