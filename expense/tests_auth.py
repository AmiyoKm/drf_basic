from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from expense.models import Transactions

class AuthTransactionTests(APITestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        # Create transactions for user1
        self.t1 = Transactions.objects.create(
            title="User1 Transaction",
            amount=100,
            transaction_type="CREDIT",
            user_id=self.user1
        )

        # Create transactions for user2
        self.t2 = Transactions.objects.create(
            title="User2 Transaction",
            amount=200,
            transaction_type="DEBIT",
            user_id=self.user2
        )

        self.list_url = '/api/transactions/'
        self.detail_url_t1 = f'/api/transactions/{self.t1.id}/'
        self.detail_url_t2 = f'/api/transactions/{self.t2.id}/'

    def test_unauthenticated_access(self):
        """Ensure unauthenticated users cannot access transactions."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_transactions(self):
        """Ensure user sees only their own transactions."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['title'], "User1 Transaction")

    def test_create_transaction(self):
        """Ensure created transaction is associated with the authenticated user."""
        self.client.force_authenticate(user=self.user1)
        data = {
            "title": "New Transaction",
            "amount": 50,
            "transaction_type": "CREDIT"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transactions.objects.filter(user_id=self.user1).count(), 2)
        self.assertEqual(Transactions.objects.get(title="New Transaction").user_id, self.user1)

    def test_access_other_user_transaction(self):
        """Ensure user cannot access another user's transaction."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.detail_url_t2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_transaction(self):
        """Ensure user can update their own transaction."""
        self.client.force_authenticate(user=self.user1)
        data = {"amount": 150}
        response = self.client.patch(self.detail_url_t1, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.t1.refresh_from_db()
        self.assertEqual(self.t1.amount, 150)

    def test_delete_own_transaction(self):
        """Ensure user can delete their own transaction."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.detail_url_t1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Transactions.objects.filter(id=self.t1.id).exists())
