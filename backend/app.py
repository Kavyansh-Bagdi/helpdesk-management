import os
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_migrate import Migrate
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
from dotenv import load_dotenv
from flask_cors import CORS

from models import db, Users, Tickets, Comments, TicketImages

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)



# Decorator for token verification
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.get(data['id'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Authentication Routes
@app.route('/api/images/<int:image_id>')
def get_image(image_id):
    image = TicketImages.query.get_or_404(image_id)
    return Response(image.image_data, mimetype='image/jpeg')

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    new_user = Users(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username, 'email': new_user.email, 'role': new_user.role}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Users.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({'token': token})

# Tickets Routes
@app.route('/api/tickets', methods=['GET'])
@token_required
def get_tickets(current_user):
    if current_user.role in ['admin', 'agent']:
        tickets = Tickets.query.all()
    else:
        tickets = Tickets.query.filter_by(author_id=current_user.id).all()
    
    output = []
    for ticket in tickets:
        ticket_data = {
            'id': ticket.id,
            'title': ticket.title,
            'description': ticket.description,
            'status': ticket.status,
            'author_id': ticket.author_id,
            'created_at': ticket.created_at.isoformat(),
            'image_ids': [image.id for image in ticket.images]
        }
        output.append(ticket_data)
    
    return jsonify(output)

@app.route('/api/tickets', methods=['POST'])
@token_required
def create_ticket(current_user):
    title = request.form.get('title')
    description = request.form.get('description')
    images = request.files.getlist('images')

    if not title or not description:
        return jsonify({'message': 'Title and description are required!'}), 400

    new_ticket = Tickets(title=title, description=description, author_id=current_user.id)
    db.session.add(new_ticket)
    db.session.commit()

    image_ids = []
    if images:
        for image in images:
            image_data = image.read()
            new_image = TicketImages(ticket_id=new_ticket.id, image_data=image_data)
            db.session.add(new_image)
            db.session.commit()
            image_ids.append(new_image.id)

    ticket_data = {
        'id': new_ticket.id,
        'title': new_ticket.title,
        'description': new_ticket.description,
        'status': new_ticket.status,
        'author_id': new_ticket.author_id,
        'created_at': new_ticket.created_at.isoformat(),
        'image_ids': image_ids
    }
    
    return jsonify(ticket_data), 201

@app.route('/api/tickets/<int:ticket_id>', methods=['GET'])
@token_required
def get_ticket(current_user, ticket_id):
    ticket = Tickets.query.get_or_404(ticket_id)
    
    if current_user.role not in ['admin', 'agent'] and ticket.author_id != current_user.id:
        return jsonify({'message': 'Cannot perform that function!'}), 403
        
    ticket_data = {
        'id': ticket.id,
        'title': ticket.title,
        'description': ticket.description,
        'status': ticket.status,
        'author_id': ticket.author_id,
        'created_at': ticket.created_at.isoformat(),
        'image_ids': [image.id for image in ticket.images]
    }
    
    return jsonify(ticket_data)

@app.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
@token_required
def update_ticket(current_user, ticket_id):
    ticket = Tickets.query.get_or_404(ticket_id)
    
    if current_user.role not in ['admin', 'agent']:
        return jsonify({'message': 'Cannot perform that function!'}), 403
        
    data = request.get_json()
    ticket.status = data.get('status', ticket.status)
    db.session.commit()
    
    ticket_data = {
        'id': ticket.id,
        'title': ticket.title,
        'description': ticket.description,
        'status': ticket.status,
        'author_id': ticket.author_id,
        'created_at': ticket.created_at.isoformat()
    }
    
    return jsonify(ticket_data)

# Comments Routes
@app.route('/api/tickets/<int:ticket_id>/comments', methods=['GET'])
@token_required
def get_comments(current_user, ticket_id):
    ticket = Tickets.query.get_or_404(ticket_id)
    
    if current_user.role not in ['admin', 'agent'] and ticket.author_id != current_user.id:
        return jsonify({'message': 'Cannot perform that function!'}), 403
        
    comments = Comments.query.filter_by(ticket_id=ticket_id).all()
    output = []
    for comment in comments:
        comment_data = {
            'id': comment.id,
            'text': comment.text,
            'author_id': comment.author_id,
            'ticket_id': comment.ticket_id,
            'created_at': comment.created_at.isoformat()
        }
        output.append(comment_data)
        
    return jsonify(output)

@app.route('/api/tickets/<int:ticket_id>/comments', methods=['POST'])
@token_required
def add_comment(current_user, ticket_id):
    ticket = Tickets.query.get_or_404(ticket_id)
    
    if current_user.role not in ['admin', 'agent'] and ticket.author_id != current_user.id:
        return jsonify({'message': 'Cannot perform that function!'}), 403
        
    data = request.get_json()
    new_comment = Comments(text=data['text'], author_id=current_user.id, ticket_id=ticket_id)
    db.session.add(new_comment)
    db.session.commit()
    
    comment_data = {
        'id': new_comment.id,
        'text': new_comment.text,
        'author_id': new_comment.author_id,
        'ticket_id': new_comment.ticket_id,
        'created_at': new_comment.created_at.isoformat()
    }
    
    return jsonify(comment_data), 201

if __name__ == '__main__':
    app.run(debug=True)
