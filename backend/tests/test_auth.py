
import json
import pytest
from app import db
from models import Users

def test_register(client, init_database):
    """Test user registration."""
    response = client.post('/api/auth/register', 
                           data=json.dumps(dict(
                               username='testuser',
                               email='test@example.com',
                               password='password'
                           )),
                           content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'
    assert 'id' in data

def test_login(client, init_database):
    """Test user login."""
    # First, register a user
    client.post('/api/auth/register', 
                data=json.dumps(dict(
                    username='testuser',
                    email='test@example.com',
                    password='password'
                )),
                content_type='application/json')

    # Now, log in
    response = client.post('/api/auth/login',
                           data=json.dumps(dict(
                               email='test@example.com',
                               password='password'
                           )),
                           content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data

def test_login_invalid_credentials(client, init_database):
    """Test login with invalid credentials."""
    response = client.post('/api/auth/login',
                           data=json.dumps(dict(
                               email='wrong@example.com',
                               password='wrongpassword'
                           )),
                           content_type='application/json')
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['message'] == 'Invalid credentials'
