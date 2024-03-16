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

    if os.path.exists(filename):
        os.remove(filename)

    username_key = "username"
    nickname_key = "nick"
    discord_id_key = "discord_id"
    hangout_title = "Haltise Extravaganza"

    time_now_in_seconds = int(datetime.now().timestamp())
    duration_in_minutes = 60  # 60 minutes
    duration_in_seconds = duration_in_minutes * 60

    data = {
        # "filename": filename, <- filename not added to the json file by create
        "hangout_name": hangout_title,
        "duration": 60,
        "maker": {username_key: "haltiseelyokade", discord_id_key: 1015276712948400148},  # username instead of nickname
        "participants": [  # converts participants into a list and includes the maker
            {nickname_key: "Haltise", discord_id_key: 1015276712948400148},
            {nickname_key: "Zatch", discord_id_key: 583730259409633310},
            {nickname_key: "Kyo", discord_id_key: 309330832047210497},
            {nickname_key: "Berenger", discord_id_key: 319472632493768705},
        ],
        "subtasks": [  # converts subtasks into a list
            {'subtask': "Task A", 'finished': False},
            {'subtask': "Task Z", 'finished': False},
            {'subtask': "Task W", 'finished': False},
            {'subtask': "Task P", 'finished': False},
            {'subtask': "Task Q", 'finished': False}
        ],
        'start_time': time_now_in_seconds,  # create function adds this
        'end_time': time_now_in_seconds + duration_in_seconds  # create function adds this
    }

    with open(filename, mode='w', encoding='utf-8') as f:
        json.dump([data], f)  # notice the data was dumped as an element of a list

    result = prog_backend.read_session(filename, hangout_title)
    # The result should more or less be exactly like the data
    for key, value in data.items():
        assert key in result
        assert type(data[key]) == type(result[key])
        if not isinstance(result[key], dict) and not isinstance(result[key], list):
            assert result[key] == data[key]
        if isinstance(result[key], dict):
            assert key == "maker"
        if isinstance(result[key], list):
            # Sort the list of dictionaries within data and data2
            sorted_expected = sorted(data[key], key=lambda d: sorted(d.items()))
            sorted_actual = sorted(result[key], key=lambda d: sorted(d.items()))

            # Compare the sorted lists of dictionaries
            assert sorted_expected == sorted_actual


