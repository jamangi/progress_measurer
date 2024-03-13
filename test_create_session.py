import json
import prog_backend
import os


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
        "subtask4": "Task 4",
        "subtask5": "Task 5"
    }

    data2 = {
        "filename": filename,
        "hangout_name": hangout_title,
        "duration": 60,
        "maker": {username_key: "JimJam", discord_id_key: 1},
        "participant2": {username_key: "Jack", discord_id_key: 2},
        "participant3": {username_key: "Jill", discord_id_key: 3},
        "participant4": {username_key: "Princess Peach", discord_id_key: 4},
        "subtask1": "Task 1",
        "subtask2": "Task 2",
        "subtask3": "Task 3",
        "subtask4": "Task 4",
        "subtask5": "Task 5"
    }

    #######################
    #######################

    expected_data = [data2]

    prog_backend.create_session(**data1) # requires keyword args

    # check json
    with open(filename, mode='r', encoding='utf-8') as f:
        res = json.load(f)
        assert isinstance(res, list) and res[0] == expected_data[0]
