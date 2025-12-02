
import json
import pytest
from app import db
from models import Users, Tickets
import io

def get_auth_token(client):
    """Helper function to get an auth token."""
    client.post('/api/auth/register', 
                data=json.dumps(dict(
                    username='testuser',
                    email='test@example.com',
                    password='password'
                )),
                content_type='application/json')
    response = client.post('/api/auth/login',
                           data=json.dumps(dict(
                               email='test@example.com',
                               password='password'
                           )),
                           content_type='application/json')
    return json.loads(response.data)['token']

def test_create_ticket(client, init_database):
    """Test ticket creation."""
    token = get_auth_token(client)
    response = client.post('/api/tickets',
                           headers={'Authorization': f'Bearer {token}'},
                           data={
                               'title': 'Test Ticket',
                               'description': 'This is a test ticket.',
                               'images': (io.BytesIO(b"some initial text data"), 'test.jpg')
                           },
                           content_type='multipart/form-data')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test Ticket'
    assert data['description'] == 'This is a test ticket.'
    assert 'id' in data
    assert 'image_ids' in data
    assert len(data['image_ids']) == 1

def test_get_tickets(client, init_database):
    """Test getting tickets."""
    token = get_auth_token(client)
    client.post('/api/tickets',
                headers={'Authorization': f'Bearer {token}'},
                data={
                    'title': 'Test Ticket',
                    'description': 'This is a test ticket.'
                },
                content_type='multipart/form-data')
    
    response = client.get('/api/tickets', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['title'] == 'Test Ticket'

def test_get_ticket(client, init_database):
    """Test getting a single ticket."""
    token = get_auth_token(client)
    create_response = client.post('/api/tickets',
                                  headers={'Authorization': f'Bearer {token}'},
                                  data={
                                      'title': 'Test Ticket',
                                      'description': 'This is a test ticket.'
                                  },
                                  content_type='multipart/form-data')
    ticket_id = json.loads(create_response.data)['id']
    
    response = client.get(f'/api/tickets/{ticket_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Test Ticket'
    assert data['id'] == ticket_id

def test_update_ticket(client, init_database):
    """Test updating a ticket."""
    # Register an admin user
    client.post('/api/auth/register', 
                data=json.dumps(dict(
                    username='adminuser',
                    email='admin@example.com',
                    password='password'
                )),
                content_type='application/json')
    
    with client.application.app_context():
        admin_user = Users.query.filter_by(email='admin@example.com').first()
        admin_user.role = 'admin'
        db.session.commit()

    # Log in as admin
    response = client.post('/api/auth/login',
                           data=json.dumps(dict(
                               email='admin@example.com',
                               password='password'
                           )),
                           content_type='application/json')
    admin_token = json.loads(response.data)['token']

    # Register a regular user and create a ticket
    user_token = get_auth_token(client)
    create_response = client.post('/api/tickets',
                                  headers={'Authorization': f'Bearer {user_token}'},
                                  data={
                                      'title': 'Test Ticket',
                                      'description': 'This is a test ticket.'
                                  },
                                  content_type='multipart/form-data')
    ticket_id = json.loads(create_response.data)['id']

    # Update the ticket as admin
    response = client.put(f'/api/tickets/{ticket_id}',
                          headers={'Authorization': f'Bearer {admin_token}'},
                          data=json.dumps(dict(status='closed')),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'closed'
