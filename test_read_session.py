import json
import prog_backend
import os
from datetime import datetime


def test_read_json():
    # delete database if it exists
    # put data into the json file
    # - could look like data2 from the test_create file
    # use the read function to read it
    # ensure the returned data is formatted correctly

    filename = "test_database.json"


    username_key = "username"
    nickname_key = "nick"
    discord_id_key = "discord_id"
    hangout_title = "Hangout Sample"

    data2 = {
        # "filename": filename, <- filename not added to the json file by create
        "hangout_name": hangout_title,
        "duration": 60,
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
            # {'subtask': None, 'finished': False} # This task isn't included since it was None
        ],
        'start_time': int(datetime.now().timestamp()),  # create function adds this
        'end_time': None  # create function adds this
    }

    with open(filename, mode='w', encoding='utf-8') as f:
        json.dump([data2], f)

    result = prog_backend.read_session(filename, hangout_title)
