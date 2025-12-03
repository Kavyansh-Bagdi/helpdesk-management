
import json
import pytest
from app import db
from models import Users, Tickets
import io

def get_auth_token(client, username='testuser', email='test@example.com'):
    client.post('/api/auth/register', 
                data=json.dumps(dict(
                    username=username,
                    email=email,
                    password='password'
                )),
                content_type='application/json')
    response = client.post('/api/auth/login',
                           data=json.dumps(dict(
                               email=email,
                               password='password'
                           )),
                           content_type='application/json')
    return json.loads(response.data)['token']

def test_add_comment(client, init_database):
    token = get_auth_token(client)
    create_response = client.post('/api/tickets',
                                  headers={'Authorization': f'Bearer {token}'},
                                  data={
                                      'title': 'Test Ticket',
                                      'description': 'This is a test ticket.'
                                  },
                                  content_type='multipart/form-data')
    ticket_id = json.loads(create_response.data)['id']

    response = client.post(f'/api/tickets/{ticket_id}/comments',
                           headers={'Authorization': f'Bearer {token}'},
                           data=json.dumps(dict(text='This is a test comment.')),
                           content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['text'] == 'This is a test comment.'
    assert data['ticket_id'] == ticket_id

def test_get_comments(client, init_database):
    token = get_auth_token(client)
    create_response = client.post('/api/tickets',
                                  headers={'Authorization': f'Bearer {token}'},
                                  data={
                                      'title': 'Test Ticket',
                                      'description': 'This is a test ticket.'
                                  },
                                  content_type='multipart/form-data')
    ticket_id = json.loads(create_response.data)['id']
    client.post(f'/api/tickets/{ticket_id}/comments',
                headers={'Authorization': f'Bearer {token}'},
                data=json.dumps(dict(text='This is a test comment.')),
                content_type='application/json')

    response = client.get(f'/api/tickets/{ticket_id}/comments',
                          headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['text'] == 'This is a test comment.'

def test_get_image(client, init_database):
    token = get_auth_token(client)
    create_response = client.post('/api/tickets',
                                  headers={'Authorization': f'Bearer {token}'},
                                  data={
                                      'title': 'Test Ticket',
                                      'description': 'This is a test ticket.',
                                      'images': (io.BytesIO(b'test image data'), 'test.jpg')
                                  },
                                  content_type='multipart/form-data')
    image_id = json.loads(create_response.data)['image_ids'][0]

    response = client.get(f'/api/images/{image_id}')
    assert response.status_code == 200
    assert response.mimetype == 'image/jpeg'
    assert response.data == b'test image data'
