import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app import create_app
from config_test import TestConfig
from main import db
from tests import BaseTestCase
from main.models import EventModel as Event
from tests.constants import event_data_1, event_data_2, event_data_3
from main.services import EventService


class TestEventController(BaseTestCase):
    '''
    Test the Event controllers
    '''

    def setUp(self):
        '''
        Setup the test case and create the initial event data
        '''

        # Call the parent method
        super().setUp()

        # Create the initial event data
        event_1 = Event(**event_data_1) # type: ignore
        event_2 = Event(**event_data_2) # type: ignore
        event_3 = Event(**event_data_3) # type: ignore
    

        # Add the event data to the database
        db.session.add(event_1)
        db.session.add(event_2)
        db.session.add(event_3)
        db.session.commit()

    def test_get_events(self):
        '''
        Test the GET /events controller
        '''
        # Make a GET request to the /events route
        response = self.client.get('/api/events')
        self.assertEqual(response.status_code, 200)

        # Verify that the response is a list
        self.assertIsInstance(response.json, list)
        
        # Check that each item in the list has the expected keys
        for event in response.json:
            self.assertIn('code', event)
            self.assertIn('name', event)
            self.assertIn('description', event)
            self.assertIn('date', event)
            self.assertIn('location', event)
            self.assertIn('capacity', event)
            self.assertIn('total_inscriptions', event)

    def test_get_event(self):
        '''
        Test the GET /events/<event_code> controller
        '''
        # Get the first event from the database
        event = Event.query.first()

        # Make a GET request to the /events/<id> route
        response = self.client.get(f'/api/events/{event.event_code}')
        self.assertEqual(response.status_code, 200)
        # Verify that the response has the expected keys
        self.assertIn('code', response.json)
        self.assertIn('name', response.json)
        self.assertIn('description', response.json)
        self.assertIn('date', response.json)
        self.assertIn('location', response.json)
        self.assertIn('capacity', response.json)
        self.assertIn('total_inscriptions', response.json)



class TestEventServices(unittest.TestCase):
    """
    Test the EventService methods
    """

    def setUp(self):
        """
        Setup the test case with a mocked repository
        """
        self.mock_repo = MagicMock()
        self.event_service = EventService()
        self.event_service._EventService__repository = self.mock_repo

    def test_create_event(self):
        """
        Test the create method of EventService
        """
        mock_event = MagicMock()
        mock_event.name = 'Test Event'
        mock_event.event_code = 'E004'
        self.mock_repo.create.return_value = mock_event

        result = self.event_service.create(
            event_code='E004',
            name='Test Event',
            description='This is a test event.',
            date='2024-12-31 23:59:59',
            location='Test Location',
            capacity=100
        )

        self.mock_repo.create.assert_called_once()
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'Test Event')
        self.assertEqual(result.event_code, 'E004')

    def test_find_all_events(self):
        """
        Test the find_all method of EventService
        """
        mock_event_1 = MagicMock()
        mock_event_1.name = 'Event 1'
        mock_event_2 = MagicMock()
        mock_event_2.name = 'Event 2'
        self.mock_repo.find_all.return_value = [mock_event_1, mock_event_2]

        result = self.event_service.find_all()

        self.mock_repo.find_all.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, 'Event 1')

    def test_find_event_by_id(self):
        """
        Test the find_by_id method of EventService
        """
        mock_event = MagicMock()
        mock_event.id = 1
        mock_event.name = 'Event 1'
        self.mock_repo.find_by_id.return_value = mock_event

        result = self.event_service.find_by_id(1)

        self.mock_repo.find_by_id.assert_called_once_with(1)
        self.assertEqual(result.name, 'Event 1')

    def test_find_event_by_id_not_found(self):
        """
        Test the find_by_id method when event does not exist
        """
        self.mock_repo.find_by_id.return_value = None

        result = self.event_service.find_by_id(999)

        self.mock_repo.find_by_id.assert_called_once_with(999)
        self.assertIsNone(result)

    def test_update_event(self):
        """
        Test the update method of EventService
        """
        mock_updated_event = MagicMock()
        mock_updated_event.name = 'Updated Event'
        mock_updated_event.location = 'Updated Location'
        self.mock_repo.update.return_value = mock_updated_event

        result = self.event_service.update(
            id=1,
            event_code='E001',
            name='Updated Event',
            description='This is an updated event.',
            date='2024-12-31 23:59:59',
            location='Updated Location',
            capacity=200
        )

        self.mock_repo.update.assert_called_once()
        self.assertEqual(result.name, 'Updated Event')
        self.assertEqual(result.location, 'Updated Location')

    def test_delete_event(self):
        """
        Test the delete method of EventService
        """
        self.mock_repo.delete.return_value = True

        result = self.event_service.delete(1)

        self.mock_repo.delete.assert_called_once_with(1)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
