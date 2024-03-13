"""A bunch of functions that do important stuff in the background

import os
import json
from datetime import datetime


def create_session(filename, hangout_name, duration, maker, subtask1,
participant2=None, participant3=None, participant4=None):
    Organizes the session into a dict and then adds that dict to the json file
    
    :param filename: (str)
    :param hangout_name: (str)
    :param duration: (int)
    :param maker: (user object)
    :param subtask1: (str)
    :param subtask2: (str)
    :param subtask3: (str)
    :param subtask4: (str)
    :param subtask5: (str)
    :param participant2: (user object) (optional)
    :param participant3: (user object) (optional)
    :param participant4: (user object) (optional)

    # Make sure the database file is already there. If it's not, create it
    if not os.path.isfile(filename) or not os.path.isfile(filename):
        with open(filename, 'w') as new_json:
            json.dump([], new_json)

    # Set up start_time and participants so they're ready to be added to the entry
    start_time = datetime.now().timestamp()
    participants = [{'nick': maker.display_name, 'discord_id': int(maker.id)}]
    if participant2:
        participants.append({'nick': participant2.display_name, 'discord_id': participant2.id})
    if participant3:
        participants.append({'nick': participant3.display_name, 'discord_id': participant3.id})
    if participant4:
        participants.append({'nick': participant4.display_name, 'discord_id': participant4.id})

    # Create the entry
    new_entry = {'hangout_name': hangout_name,
                 'duration': duration,
                 'maker': {'username': maker.username, 'discord_id': int(maker.id)},
                 'participants': participants,
                 'subtasks': [{'subtask': subtask1, 'finished': False},
                              {'subtask': subtask2, 'finished': False},
                              {'subtask': subtask3, 'finished': False},
                              {'subtask': subtask4, 'finished': False},
                              {'subtask': subtask5, 'finished': False}],
                 'start_time': start_time,
                 'end_time': start_time + duration
                 }
    # Read all entries in the json, then add a new one
    with open(filename, "r") as entries_file:
        entries = json.load(entries_file)
    entries.append(new_entry)
    with open(filename, "w") as entries_file:
        json.dump(entries, entries_file)"""

#____________________________________MIMOSA's property________________________________________
import os
import json
from datetime import datetime

# Function to create the JSON file if it doesn't exist
def create_json_if_not_exists(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as new_json:
            json.dump([], new_json)

# Function to create a session entry
def create_session(filename, hangout_name, duration, maker, *participants, **kwargs):
    participants_list = []
    subtasks = []

    for key, value in kwargs.items():
        if key.startswith("participant"):
            participants_list.append(value)
        elif key.startswith("subtask"):
            subtasks.append(value)

    data = {
        "hangout_name": hangout_name,
        "duration": duration,
        "maker": {"username": maker.username, "id": maker.id, "display_name": maker.display_name} if hasattr(maker, 'username') else maker,
        "participants": [
            {"username": participant.get("username", ""), "id": participant.get("id", ""), "display_name": participant.get("display_name", "")}
            if isinstance(participant, dict) else {"username": participant.username, "id": participant.id, "display_name": participant.display_name}
            for participant in participants_list
        ],
        "subtasks": [{"subtask": task, "finished": False} for task in subtasks if task is not None],
        "start_time": int(datetime.now().timestamp()),
        "end_time": None
    }

    with open(filename, 'r+') as f:
        entries = json.load(f)
        entries.append(data)
        f.seek(0)
        json.dump(entries, f)

# Example usage:
filename = "test_database.json"
create_json_if_not_exists(filename)

# Creating a session entry with dictionary participants
create_session(filename, "Sample Hangout", 60, {"username": "TestUser", "id": 1, "display_name": "JimJam"},
               participant1={"username": "User1", "id": 1, "display_name": "User1"},
               participant2={"username": "User2", "id": 2, "display_name": "User2"},
               subtask1="Task 1",
               subtask2="Task 2")
def create_json_if_not_exists(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as new_json:
            json.dump([], new_json)