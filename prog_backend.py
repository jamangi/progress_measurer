import json
from typing import Any, Dict, List, Optional
"""A bunch of functions that do important stuff in the background"""

import os
import json
from datetime import datetime


def create_session(filename, hangout_name, duration, maker, subtask1, subtask2, subtask3, subtask4, subtask5,
                   participant2=None, participant3=None, participant4=None):
    """Organizes the session into a dict and then adds that dict to the json file
    
    :param filename: (str) the name of the file (which is in the cwd), plus .json
    :param hangout_name: (str) the name given to the session
    :param duration: (float) the number of minutes the session will last
    :param maker: (user object) discord info for the person who made the session (and as such, participant1)
    :param subtask1: (str) one of the subtasks that will be tackled in the session
    :param subtask2: (str) one of the subtasks that will be tackled in the session
    :param subtask3: (str) one of the subtasks that will be tackled in the session
    :param subtask4: (str) one of the subtasks that will be tackled in the session
    :param subtask5: (str) one of the subtasks that will be tackled in the session
    :param participant2: (user object) (optional) Discord info for another participant in the session
    :param participant3: (user object) (optional) Discord info for another participant in the session
    :param participant4: (user object) (optional) Discord info for another participant in the session
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
                 'end_time': int(start_time + duration*60)
                 }

    # Read all entries in the json, then add a new one
    with open(filename, "r") as entries_file:
        entries = json.load(entries_file)
    entries.append(new_entry)
    with open(filename, "w") as entries_file:
        json.dump(entries, entries_file)




def read_session(filename: str, hangout_name: str) -> Dict[str, Any]:
    """
    Read session data from a JSON file.

    Args:
        filename (str): The name of the JSON file to read.
        hangout_name (str): The name of the hangout to read data for.

    Returns:
        dict: The session data for the specified hangout.
    """
    with open(filename, 'r') as file:
        sessions = json.load(file)

    # Find the session data for the specified hangout name
    for session in sessions:
        if session.get('hangout_name') == hangout_name:
            return session

    # If no session found for the specified hangout name
    raise ValueError(f"No session found for hangout: {hangout_name}")


def edit_value(filename: str, session_name: str, field: str, new_value,
               subfield=None, subsubfield=None, change=None):
    """
    Edit a value in the session data for a specific hangout in the JSON file.

    Raises:
        ValueError: If the session name is not found in the JSON file.
    """
    with open(filename, 'r+') as file:
        sessions = json.load(file)

        for session in sessions:
            if session.get('hangout_name') == session_name:
                if subfield is None:
                    if change == 'add':
                        session[field].append(new_value)
                    elif change == 'remove':
                        # Check if participant exists before removing
                        participant_found = False
                        for participant in session[field]:
                            if participant == new_value:
                                session[field].remove(participant)
                                participant_found = True
                                break
                        if not participant_found:
                            raise ValueError(f"Participant {new_value} not found in session participants.")
                    else:
                        session[field] = new_value
                else:
                    if subsubfield is None:
                        session[field][subfield] = new_value
                    else:
                        session[field][subfield][subsubfield] = new_value

                # Adjust end_time if duration or start_time is changed
                if field == 'duration' or field == 'start_time':
                    session['end_time'] = session['start_time'] + session['duration'] * 60

                with open(filename, 'w') as file:
                    json.dump(sessions, file, indent=4)
                break

        else:
            raise ValueError(f"No session found with name: {session_name}")