import os
import json

#use os module to check if this reminder.json exists
def reminder_json_exists():
    return os.path.isfile('reminder.json') #check if THIS file exists ret:bool

#fetch reminders from the kjson
def read_reminder_json():
    if reminder_json_exists(): #check for file
        with open('reminder.json') as reminder_json:
            data = json.load(reminder_json) #creates a dictionary called data after parsing
            return data['reminders'] #return key
    else:
        return {} #empty dictionary

#creates a reminder dictionary
def create_reminder_json(reminder):
    if not reminder_json_exists(): #if argument does not exist, create new 
        data = {} #dict called data
        data['reminders'] = [] #value of the key 'reminders' is a list
        data['reminders'].append(reminder) #add the reminder to the list
        write_reminder_json(data) 
    else:
        update_reminder_json(reminder)

#accepts reminder and appends to the list
def update_reminder_json(reminder):
    with open('reminder.json') as reminder_json:
        data = json.load(reminder_json) #parse
        reminders = data['reminders'] #reminders = keyvalue (list)
        reminders.append(reminder) #append to list
        write_reminder_json(data)

#write JSON representation of reminders to the reminder.json
def write_reminder_json(data, filename='reminder.json'):
    with open(filename, 'w') as outfile: #writing mode
        json.dump(data, outfile, indent=4) #transforms data dictionary into a json string which is saved to the file
