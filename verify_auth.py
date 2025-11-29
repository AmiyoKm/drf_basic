import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS += ['testserver']

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def verify_auth():
    # Create test user
    username = 'testuser_auth_verify'
    password = 'testpassword123'
    if User.objects.filter(username=username).exists():
        User.objects.get(username=username).delete()

    user = User.objects.create_user(username=username, password=password)
    print(f"Created user: {username}")

    client = APIClient()
    url = '/api/transactions/'

    # Test 1: No Auth
    print("\nTest 1: No Authentication")
    response = client.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 401:
        print("PASS: Correctly denied unauthenticated access.")
    else:
        print(f"FAIL: Expected 401, got {response.status_code}")

    # Test 2: JWT Auth
    print("\nTest 2: JWT Authentication")
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    response = client.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("PASS: JWT Authentication successful.")
    else:
        print(f"FAIL: Expected 200, got {response.status_code}")
        print(response.data)

    # Test 3: Session Auth (Simulated via force_login)
    print("\nTest 3: Session Authentication")
    client.credentials() # Clear headers
    client.force_login(user)
    response = client.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("PASS: Session Authentication successful.")
    else:
        print(f"FAIL: Expected 200, got {response.status_code}")
        print(response.data)

    # Cleanup
    user.delete()

if __name__ == '__main__':
    try:
        verify_auth()
    except Exception as e:
        print(f"An error occurred: {e}")
