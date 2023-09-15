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
        }
        
    def test_timeframe_crud_operations(self):
        # Helper function to prepare and post data
        def post_entry(data):
            return self.client.post(reverse('add_entry'), data)
        
        # Successful creation, expect 201 status code
        response = post_entry(self.entry_data)
        self.assertEqual(response.status_code, 201)
        
        # Create wrong timeframe data expect 207
        #invalid_timeframe_data = {
        #    'title': 'Test Title',
        #    'description': 'Test Description',
        #    'start_time': datetime.now() + timedelta(hours=-2),
        #    'end_time': datetime.now()
        #}
        #response = post_entry(invalid_timeframe_data)
        #self.assertEqual(response.status_code, 207)
        
        # Create correct timeframe
        timeframe_data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'start_time': datetime.now()
        }
        response = post_entry(timeframe_data)
        self.assertEqual(response.status_code, 201)

        # Create correct timeframe
        timeframe_data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'end_time': datetime.now()
        }
        response = post_entry(timeframe_data)
        self.assertEqual(response.status_code, 201)

        # Convert the 'start_time' and 'end_time' from the POST data to timezone aware datetime objects
        start_time = self.entry_data['start_time'].replace(tzinfo=timezone.utc)
        end_time = self.entry_data['end_time'].replace(tzinfo=timezone.utc)

        # Read and check if the entry was added to the database
        entries = Entry.objects.all()
        self.assertEqual(len(entries), 3)
        self.assertEqual(entries[0].title, 'Test Title')
        self.assertEqual(entries[0].time_frame.start_time, start_time)  # Verify 'start_time' matches
        self.assertEqual(entries[0].time_frame.end_time, end_time)      # Verify 'end_time' matches

        # 3. Attempt to update the previously created entry
        start_time_updated = datetime.now() + timedelta(days=1)
        end_time_updated = start_time_updated + timedelta(hours=2)

        update_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'start_time': start_time_updated,
            'end_time': end_time_updated
        }
        response = self.client.post(reverse('edit_entry', args=[entries[0].id]), update_data)
        # Expect a 200 status code if the update was successful
        self.assertEqual(response.status_code, 200)

        # Convert the updated times to timezone aware datetime objects
        start_time_updated = self.entry_data['start_time'].replace(tzinfo=timezone.utc)
        end_time_updated = self.entry_data['end_time'].replace(tzinfo=timezone.utc)

        # 4. Read and check if the entry was updated in the database
        updated_entry = Entry.objects.get(id=entries[0].id)
        self.assertEqual(updated_entry.title, 'Updated Title')
        self.assertEqual(updated_entry.time_frame.start_time, start_time_updated)  # Verify updated 'start_time'
        self.assertEqual(updated_entry.time_frame.end_time, end_time_updated)      # Verify updated 'end_time'

        # 5. Attempt to delete all entries
        for entry in entries:
            response = self.client.post(reverse('delete_entry', args=[entry.id]))
            # Expect a 302 status code after a successful deletion for each entry
            self.assertEqual(response.status_code, 302)


        # 6. Check if the entry was successfully deleted from the database
        self.assertEqual(Entry.objects.count(), 0)



    def test_entry_crud_operations(self):
        # 1. Create an entry
        response = self.client.post(reverse('add_entry'), self.entry_data)
        self.assertEqual(response.status_code, 201)  # Expecting a redirect after creation

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

