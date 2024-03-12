import json
import prog_frontend
import os


def test_create_json():
    filename = "test_database.json"

    if os.path.exists(filename):
        os.remove(filename)

    username_key = "username"
    discord_id_key = "discord_id"
    hangout_title = "Sample Hangout"
    hangout_title2 = "Sample Hangout 2"
    data1 = {
        "filename": filename,
        "hangout_name": hangout_title,
        "duration": 60,
        "maker": "TestUser",
        "participant2": {username_key: "User2", discord_id_key: 2},
        "participant3": {username_key: "User3", discord_id_key: 3},
        "participant4": {username_key: "User4", discord_id_key: 4},
        "subtask1": "Task 1",
        "subtask2": "Task 2",
        "subtask3": "Task 3",
        "subtask4": "Task 4",
        "subtask5": "Task 5"
    }

    data2 = {
        "filename": filename,
        "hangout_name": hangout_title2,
        "duration": 60,
        "maker": "TestUser",
        "participant2": {username_key: "User2", discord_id_key: 2},
        "participant3": {username_key: "User3", discord_id_key: 3},
        "participant4": {username_key: "User4", discord_id_key: 4},
        "subtask1": "Task 1",
        "subtask2": "Task 2",
        "subtask3": "Task 3",
        "subtask4": "Task 4",
        "subtask5": "Task 5"
    }

    alldata = [data1, data2]
    prog_frontend.create_session(**data1) # requires keyword args
    prog_frontend.create_session(**data2)
    with open(filename, mode='r', encoding='utf-8') as f:
        res = json.load(f)
        assert len(res) and res[0] == alldata[0]
        assert len(res) == 2 and res[1] == alldata[1]
