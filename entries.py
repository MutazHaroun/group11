from flask import Blueprint, request, jsonify
from models import db, Entry

entries_blueprint = Blueprint('entries', __name__)

@entries_blueprint.route('/', methods=['POST'])
def create_entry():
    """Endpoint to create a new journal entry"""
    data = request.get_json()
    new_entry = Entry(
        title=data['title'],
        description=data['description'],
        user_id=data['userId']  # Assume userId is passed in request body
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({
        'status': 200,
        'message': 'Entry successfully created',
        'data': {
            'id': new_entry.id,
            'createdOn': new_entry.created_on,
            'title': new_entry.title,
            'description': new_entry.description
        }
    })

@entries_blueprint.route('/<int:entry_id>', methods=['PATCH'])
def modify_entry(entry_id):
    """Endpoint to modify an existing journal entry"""
    data = request.get_json()
    entry = Entry.query.get(entry_id)
    if entry:
        entry.title = data['title']
        entry.description = data['description']
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': 'Entry successfully edited',
            'data': {
                'id': entry.id,
                'title': entry.title,
                'description': entry.description
            }
        })
    return jsonify({'status': 404, 'error': 'Entry not found'})

@entries_blueprint.route('/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Endpoint to delete a journal entry"""
    entry = Entry.query.get(entry_id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({
            'status': 204,
            'message': 'Entry successfully deleted'
        })
    return jsonify({'status': 404, 'error': 'Entry not found'})

@entries_blueprint.route('/', methods=['GET'])
def view_entries():
    """Endpoint to view all journal entries sorted by descending order"""
    entries = Entry.query.order_by(Entry.created_on.desc()).all()
    entries_list = [{
        'id': entry.id,
        'createdOn': entry.created_on,
        'title': entry.title,
        'description': entry.description
    } for entry in entries]
    return jsonify({'status': 200, 'data': entries_list})

@entries_blueprint.route('/<int:entry_id>', methods=['GET'])
def view_entry(entry_id):
    """Endpoint to view a specific journal entry"""
    entry = Entry.query.get(entry_id)
    if entry:
        return jsonify({
            'status': 200,
            'data': {
                'id': entry.id,
                'createdOn': entry.created_on,
                'title': entry.title,
                'description': entry.description
            }
        })
    return jsonify({'status': 404, 'error': 'Entry not found'})
