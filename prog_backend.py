"""A bunch of functions that do important stuff in the background"""

import os
import json
from datetime import datetime


def create_session(filename, hangout_name, duration, maker, subtask1, subtask2, subtask3, subtask4, subtask5,
participant2=None, participant3=None, participant4=None):
    """Organizes the session into a dict and then adds that dict to the json file
    
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
    """
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
        json.dump(entries, entries_file)
