import os
from flask import Flask, request, jsonify, abort
from reminder_json_helper import read_reminder_json, create_reminder_json, write_reminder_json
import uuid #to produce distinct ids

app = Flask(__name__)

@app.route("/") #homepage


@app.route('/api/reminders', methods=['GET']) #only support HTTP GET method
def get_reminders():
    reminders = read_reminder_json()
    return jsonify({'reminders': reminders}) #read flask's jsonify

@app.route('/api/reminders', methods=['POST'])
def create_reminder():
    req_data = request.get_json()

    if not all(item in req_data for item in ("phone_number", "message", "due_date")): #ensure required data is present
        abort(400)

    reminder = { 
        'id': uuid.uuid4().hex,
        'phone_number': req_data['phone_number'],
        'message': req_data['message'],
        'interval': 'monthly',
        'due_date': req_data['due_date']
    }

    create_reminder_json(reminder)
    return jsonify({'reminder': reminder}), 201


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400    


@app.route('/api/reminders/<reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id): #argument
    reminders = read_reminder_json()
    #search for argument within the array read, 
    # and put it in another array
    reminder = [reminder for reminder in reminders if reminder['id'] == reminder_id] 
    if len(reminder) == 0: #not found
        abort(404)
    reminders.remove(reminder[0]) #if found, remove it from the array
    data = {} #update new reminder
    data['reminders'] = reminders 
    write_reminder_json(data)
    return jsonify({'message': 'Reminder has been removed successfully'})


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

if __name__ == '__main__':
    app.run()
