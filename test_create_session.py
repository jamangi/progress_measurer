import json
import prog_backend
import os
from datetime import datetime


class EmptyUser:
    def __init__(self, display_name=None, username=None, user_id=None):
        self.display_name = display_name
        self.username = username
        self.id = user_id


def test_create_json():
    filename = "test_database.json"

    if os.path.exists(filename):
        os.remove(filename)

    username_key = "username"
    nickname_key = "nick"
    discord_id_key = "discord_id"
    hangout_title = "Sample Hangout"

    data1 = {
        "filename": filename,
        "hangout_name": hangout_title,
        "duration": 60,
        "maker": EmptyUser(username="TestUser", user_id=1, display_name="JimJam"),
        "participant2": EmptyUser(username="TestUser2", user_id=2, display_name="Jack"),
        "participant3": EmptyUser(username="TestUser3", user_id=3, display_name="Jill"),
        "participant4": EmptyUser(username="TestUser4", user_id=4, display_name="Princess Peach"),
        "subtask1": "Task 1",
        "subtask2": "Task 2",
        "subtask3": "Task 3",
        "subtask4": "Task X",
        "subtask5": "Task Y"
    }

    time_now_in_seconds = int(datetime.now().timestamp())
    duration_in_minutes = 60  # 60 minutes
    duration_in_seconds = duration_in_minutes * 60

    data2 = {
        # "filename": filename, <- filename not added to the json file by create
        "hangout_name": hangout_title,
        "duration": duration_in_minutes,
        "maker": {username_key: "TestUser", discord_id_key: 1},  # username instead of nickname
        "participants": [  # converts participants into a list and includes the maker
            {nickname_key: "JimJam", discord_id_key: 1},
            {nickname_key: "Jack", discord_id_key: 2},
            {nickname_key: "Jill", discord_id_key: 3},
            {nickname_key: "Princess Peach", discord_id_key: 4},
        ],
        "subtasks": [  # converts subtasks into a list
            {'subtask': "Task 1", 'finished': False},
            {'subtask': "Task 2", 'finished': False},
            {'subtask': "Task 3", 'finished': False},
            {'subtask': "Task X", 'finished': False},
            {'subtask': "Task Y", 'finished': False}  # This task isn't included since it was None
        ],
        'start_time': time_now_in_seconds,  # create function adds this
        'end_time': time_now_in_seconds + duration_in_seconds  # start time + (60 minutes worth of seconds)
    }

    #######################
    #######################

    prog_backend.create_session(**data1)  # requires keyword args

    # check json
    with open(filename, mode='r', encoding='utf-8') as f:
        res = json.load(f)
        assert isinstance(res, list)
        data = res[0]  # the entry
        assert isinstance(data, dict) and data.get('maker')
        assert data.get('duration') and data['duration'] == 60
        assert data.get('maker') == data2['maker']

        # Sort the list of dictionaries within data and data2
        sorted_expected = sorted(data2.get('participants'), key=lambda d: sorted(d.items()))
        sorted_actual = sorted(data.get('participants'), key=lambda d: sorted(d.items()))

        # Compare the sorted lists of dictionaries
        assert sorted_expected == sorted_actual

        # do the same for subtasks
        sorted_expected = sorted(data2.get('subtasks'), key=lambda d: sorted(d.items()))
        sorted_actual = sorted(data.get('subtasks'), key=lambda d: sorted(d.items()))

        # Compare the sorted lists of dictionaries
        assert sorted_expected == sorted_actual

        start_time_expected = data2.get('start_time')
        start_time_actual = data.get('start_time')
        assert abs(start_time_expected - start_time_actual) < 5  # less than 5 unix time seconds off from test

        # end_time is in the dictionary but set to None
        assert 'end_time' in data
        assert abs(data.get('end_time') - start_time_actual) < duration_in_seconds + 5
        assert abs(data.get('end_time') - (start_time_actual + (duration_in_minutes * 60))) < 15
