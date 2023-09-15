from django.test import TestCase, Client
from django.urls import reverse
from journal_app.models import Entry
from django.contrib.auth.models import User
from datetime import datetime, timezone, timedelta

class EntryCRUDTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=1)

        self.entry_data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'start_time': start_time,  # TimeFrame attributes
            'end_time': end_time,
            # Add other required fields here
        }
        
    def test_entry_inclusive_timeframe_crud_operations(self):
        # 1. Create an entry
        response = self.client.post(reverse('add_entry'), self.entry_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after creation

        # 2. Read/Check if the entry was added
        entries = Entry.objects.all()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].title, 'Test Title')
        start_time=self.entry_data['start_time'].replace(tzinfo=timezone.utc)
        end_time=self.entry_data['end_time'].replace(tzinfo=timezone.utc)
        self.assertEqual(entries[0].time_frame.start_time, start_time)  # Assert TimeFrame attributes
        self.assertEqual(entries[0].time_frame.end_time, end_time)

        # 3. Update the entry
        start_time_updated = datetime.now() + timedelta(days=1)
        end_time_updated = start_time_updated + timedelta(hours=2)

        update_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'start_time': start_time_updated,  # Updated TimeFrame attributes
            'end_time': end_time_updated,
            # Add other required fields here
        }
        response = self.client.post(reverse('edit_entry', args=[entries[0].id]), update_data)
        self.assertEqual(response.status_code, 200)

        start_time_updated=self.entry_data['start_time'].replace(tzinfo=timezone.utc)
        end_time_updated=self.entry_data['end_time'].replace(tzinfo=timezone.utc)

        # 4. Read/Check if the entry was updated
        updated_entry = Entry.objects.get(id=entries[0].id)
        self.assertEqual(updated_entry.title, 'Updated Title')
        self.assertEqual(updated_entry.time_frame.start_time, start_time_updated)  # Assert TimeFrame attributes
        self.assertEqual(updated_entry.time_frame.end_time, end_time_updated)

        # 5. Delete the entry
        response = self.client.post(reverse('delete_entry', args=[entries[0].id]))
        self.assertEqual(response.status_code, 302)

        # 6. Check if the entry was deleted
        self.assertEqual(Entry.objects.count(), 0)


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

