import unittest
from unittest.mock import MagicMock
from main import db
from main.models import InscriptionModel as Inscription
from main.models import EventModel as Event
from main.models import GuestModel as Guest
from tests import BaseTestCase
from tests.constants import event_data_1, guest_data_1, inscription_data_1, inscription_data_2, inscription_data_3
from main.services import InscriptionService

class TestInscriptionController(BaseTestCase):
    """
    Test the InscriptionController controllers
    """

    def setUp(self):
        """
        Setup the test case and create the initial inscription data
        """
        super().setUp()
        self.client = self.app.test_client()

        # Create the initial event and guest in the database
        self.event = Event(**event_data_1) #type: ignore
        self.guest = Guest(**guest_data_1) #type: ignore
        db.session.add_all([self.event, self.guest])
        db.session.commit()

        # Create the initial inscription in the database
        self.inscription_1 = Inscription(**inscription_data_1) #type: ignore
        db.session.add(self.inscription_1)
        db.session.commit()

    def test_post_inscription(self):
        """
        Test the POST /events/{event_code}/inscriptions controller
        """
        inscription_data = {
            'name': 'Guest Name',
            'email': 'guestemail@example.com',
            'phone': '123456789',
            'dni': 123456789
        }
        response = self.client.post('/api/events/E001/inscriptions', json=inscription_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json)
        self.assertIn('event_code', response.json)
        self.assertIn('guest_code', response.json)

    def test_get_inscription(self):
        """
        Test the GET /events/{event_code}/inscriptions/{guest_code} controller
        """
        response = self.client.get('/api/events/E001/inscriptions/G-0001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json)
        self.assertIn('event_code', response.json)
        self.assertIn('guest_code', response.json)

    def test_delete_inscription(self):
        """
        Test the DELETE /events/{event_code}/inscriptions/{guest_code} controller
        """
        response = self.client.delete('/api/events/E001/inscriptions/G-0001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('', response.json)


class TestInscriptionServices(unittest.TestCase):
    """
    Test the InscriptionService methods
    """

    def setUp(self):
        """
        Setup the test case with a mocked repository
        """
        self.mock_repo = MagicMock()
        self.inscription_service = InscriptionService()
        self.inscription_service._InscriptionService__repository = self.mock_repo

    def test_create_inscription(self):
        """
        Test the create method of InscriptionService
        """
        mock_inscription = MagicMock()
        mock_inscription.status = 'Confirmed'
        mock_inscription.event_id = 1
        mock_inscription.guest_id = 1
        self.mock_repo.create.return_value = mock_inscription

        result = self.inscription_service.create(
            status='Confirmed',
            event_id=1,
            guest_id=1
        )

        self.mock_repo.create.assert_called_once()
        self.assertIsNotNone(result)
        self.assertEqual(result.status, 'Confirmed')

    def test_find_all_inscriptions(self):
        """
        Test the find_all method of InscriptionService
        """
        mock_insc_1 = MagicMock()
        mock_insc_1.status = 'Confirmed'
        mock_insc_2 = MagicMock()
        mock_insc_2.status = 'Pending'
        mock_insc_3 = MagicMock()
        mock_insc_3.status = 'Canceled'
        self.mock_repo.find_all.return_value = [mock_insc_1, mock_insc_2, mock_insc_3]

        result = self.inscription_service.find_all()

        self.mock_repo.find_all.assert_called_once()
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].status, 'Confirmed')

    def test_find_inscription_by_id(self):
        """
        Test the find_by_id method of InscriptionService
        """
        mock_inscription = MagicMock()
        mock_inscription.id = 1
        mock_inscription.status = 'Confirmed'
        self.mock_repo.find_by_id.return_value = mock_inscription

        result = self.inscription_service.find_by_id(1)

        self.mock_repo.find_by_id.assert_called_once_with(1)
        self.assertEqual(result.status, 'Confirmed')

    def test_find_inscription_by_id_not_found(self):
        """
        Test the find_by_id method when inscription does not exist
        """
        self.mock_repo.find_by_id.return_value = None

        result = self.inscription_service.find_by_id(999)

        self.mock_repo.find_by_id.assert_called_once_with(999)
        self.assertIsNone(result)

    def test_find_by_event_guest_code(self):
        """
        Test the find_by_event_guest_code method of InscriptionService
        """
        mock_inscription = MagicMock()
        mock_inscription.status = 'Confirmed'
        self.mock_repo.find_by_event_guest_code.return_value = mock_inscription

        result = self.inscription_service.find_by_event_guest_code('E001', 'G-0001')

        self.mock_repo.find_by_event_guest_code.assert_called_once_with('E001', 'G-0001')
        self.assertEqual(result.status, 'Confirmed')

    def test_update_inscription(self):
        """
        Test the update method of InscriptionService
        """
        mock_updated = MagicMock()
        mock_updated.status = 'Canceled'
        self.mock_repo.update.return_value = mock_updated

        result = self.inscription_service.update(
            id=1,
            status='Canceled',
            event_id=1,
            guest_id=1
        )

        self.mock_repo.update.assert_called_once()
        self.assertEqual(result.status, 'Canceled')

    def test_delete_inscription(self):
        """
        Test the delete method of InscriptionService
        """
        self.mock_repo.delete.return_value = True

        result = self.inscription_service.delete(1)

        self.mock_repo.delete.assert_called_once_with(1)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
