
import json
import pytest
from app import db
from models import Users
import io

def test_full_workflow(client, init_database):
    """Test a full user workflow."""
    # 1. Register a new user
    response = client.post('/api/auth/register', 
                           data=json.dumps(dict(
                               username='workflowuser',
                               email='workflow@example.com',
                               password='password'
                           )),
                           content_type='application/json')
    assert response.status_code == 201
    user_data = json.loads(response.data)
    user_id = user_data['id']

    # 2. Log in with the new user
    response = client.post('/api/auth/login',
                           data=json.dumps(dict(
                               email='workflow@example.com',
                               password='password'
                           )),
                           content_type='application/json')
    assert response.status_code == 200
    user_token = json.loads(response.data)['token']

    # 3. Create a new ticket
    response = client.post('/api/tickets',
                           headers={'Authorization': f'Bearer {user_token}'},
                           data={
                               'title': 'Workflow Ticket',
                               'description': 'This is a ticket created during a workflow test.',
                               'images': (io.BytesIO(b'workflow image'), 'workflow.jpg')
                           },
                           content_type='multipart/form-data')
    assert response.status_code == 201
    ticket_data = json.loads(response.data)
    ticket_id = ticket_data['id']
    assert ticket_data['title'] == 'Workflow Ticket'
    assert len(ticket_data['image_ids']) == 1
    image_id = ticket_data['image_ids'][0]

    # 4. Add a comment to the ticket
    response = client.post(f'/api/tickets/{ticket_id}/comments',
                           headers={'Authorization': f'Bearer {user_token}'},
                           data=json.dumps(dict(text='This is a workflow comment.')),
                           content_type='application/json')
    assert response.status_code == 201
    comment_data = json.loads(response.data)
    assert comment_data['text'] == 'This is a workflow comment.'

    # 5. Register an admin user
    response = client.post('/api/auth/register', 
                           data=json.dumps(dict(
                               username='workflowadmin',
                               email='workflowadmin@example.com',
                               password='password'
                           )),
                           content_type='application/json')
    assert response.status_code == 201
    
    with client.application.app_context():
        admin_user = Users.query.filter_by(email='workflowadmin@example.com').first()
        admin_user.role = 'admin'
        db.session.commit()

    # 6. Log in as admin
    response = client.post('/api/auth/login',
                           data=json.dumps(dict(
                               email='workflowadmin@example.com',
                               password='password'
                           )),
                           content_type='application/json')
    assert response.status_code == 200
    admin_token = json.loads(response.data)['token']

    # 7. Admin views the ticket
    response = client.get(f'/api/tickets/{ticket_id}', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    assert json.loads(response.data)['title'] == 'Workflow Ticket'

    # 8. Admin updates the ticket's status
    response = client.put(f'/api/tickets/{ticket_id}',
                          headers={'Authorization': f'Bearer {admin_token}'},
                          data=json.dumps(dict(status='in_progress')),
                          content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.data)['status'] == 'in_progress'

    # 9. User views their updated ticket
    response = client.get(f'/api/tickets/{ticket_id}', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert json.loads(response.data)['status'] == 'in_progress'

    # 10. Admin views the comments
    response = client.get(f'/api/tickets/{ticket_id}/comments', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    assert len(json.loads(response.data)) == 1

    # 11. Get the image
    response = client.get(f'/api/images/{image_id}')
    assert response.status_code == 200
    assert response.data == b'workflow image'
