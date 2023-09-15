from django.test import TestCase, Client
from django.urls import reverse
from journal_app.models import Entry
from django.contrib.auth.models import User

class EntryCRUDTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Define some basic data for CRUD operations
        self.entry_data = {
            'title': 'Test Title',
            'description': 'Test Description',
            # Add other required fields here
        }

    def test_entry_crud_operations(self):
        # 1. Create an entry
        response = self.client.post(reverse('add_entry'), self.entry_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after creation

        # 2. Read/Check if the entry was added
        entries = Entry.objects.all()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].title, 'Test Title')

        # 3. Update the entry
        update_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            # Add other required fields here
        }
        response = self.client.post(reverse('edit_entry', args=[entries[0].id]), update_data)
        self.assertEqual(response.status_code, 200)

        # 4. Read/Check if the entry was updated
        updated_entry = Entry.objects.get(id=entries[0].id)
        self.assertEqual(updated_entry.title, 'Updated Title')

        # 5. Delete the entry
        response = self.client.post(reverse('delete_entry', args=[entries[0].id]))
        self.assertEqual(response.status_code, 302)

        # 6. Check if the entry was deleted
        self.assertEqual(Entry.objects.count(), 0)

