from notes.forms import NoteForm

from .base import BaseNoteTest


class TestContent(BaseNoteTest):

    def test_note_in_list_for_author(self):
        response = self.author_client.get(self.LIST_URL)
        notes = response.context['notes_feed']
        note_from_page = notes.get(id=self.note.id)
        self.assertEqual(note_from_page.title, self.note.title)
        self.assertEqual(note_from_page.text, self.note.text)
        self.assertEqual(note_from_page.slug, self.note.slug)
        self.assertEqual(note_from_page.author, self.note.author)

    def test_note_not_in_list_for_reader(self):
        self.assertNotIn(
            self.note,
            self.reader_client.get(self.LIST_URL).context['notes_feed']
        )

    def test_pages_contains_form(self):
        for url in (self.ADD_URL, self.EDIT_URL):
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'),
                    NoteForm
                )
