import json
from datetime import datetime


def unreported_hangouts_quickfetch(filename, user_id):
    """Get names of all hangout sessions in the json that don't have any of their tasks reported as having been
    finished, OR that have been reported on but that finished less than 24 hours ago.
    Only fetches the sessions that the user is a participant in.

    :param filename: (str) the name of the json file the data will be fetched from
    :param user_id: (int) the Discord is of the person who used the /report slash command
    :return: (list of dicts) the names of all unreported sessions, in {name: {name}, value: {name}} form
    """
    with open(filename, 'r') as file:
        sessions = json.load(file)
    # unix_24h_ago is the current time yesterday. We'll use this to disallow reporting on stuff older than 1 day ago if
    # it's already been reported on
    unix_now = datetime.now().timestamp()
    unix_24h_ago = unix_now - (24*60*60)
    entries_list = [{'name': hangout['hangout_name'], 'value': hangout['hangout_name']} for hangout in sessions
                    if user_id in [participant['discord_id'] for participant in hangout['participants']]
                    and ((any([subtask['finished'] is False for subtask in hangout['subtasks']])
                         and hangout['end_time'] >= unix_24h_ago)
                    or all([subtask['finished'] is False for subtask in hangout['subtasks']]))]

    return entries_list


def completed_entries_quickfetch(filename):
    """Get names of all hangout sessions in the json that have been reported on and thus have some subtasks recorded
    as having been finished.

    :param filename: (str) the name of the json file the data will be fetched from
    :return: (list of dicts) the names of all reported-on sessions, in {name: {name}, value: {name}} form
    """
    with open(filename, 'r') as file:
        sessions = json.load(file)
    entries_list = [{'name': hangout['hangout_name'], 'value': hangout['hangout_name']} for hangout in sessions
                    if not all([subtask['finished'] is False for subtask in hangout['subtasks']])]

    return entries_list