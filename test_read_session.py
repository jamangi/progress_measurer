import json
import prog_backend


def test_read_json():
    username_key = "username"
    discord_id_key = "discord_id"
    filename = "test_database.json"
    hangout_title = "Sample Hangout"
    hangout_title2 = "Sample Hangout 2"
    data1 = {
        "filename": filename,
        "hangout_name": hangout_title,
        "duration": 60,
        "maker": {username_key: "User1", discord_id_key: 1},
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
        "maker": {username_key: "User1", discord_id_key: 1},
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

    with open(filename, mode='w', encoding='utf-8') as f:
        json.dump(alldata, f)

    res1 = prog_backend.read_session(hangout_title)
    assert res1 == data1

    res2 = prog_backend.read_session(hangout_title2)
    assert res2 == data2
