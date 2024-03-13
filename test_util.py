"""Functions that create or delete example json files for use by tests"""

import json
import os

test_database_name = 'database_for_testing.json'


def make_example_database():
    # Prepare entries
    entry1 = {'hangout_name': 'Sample Hangout',
              'duration': 60,
              "maker": {"username": "User1", "discord_id": 1},
              'participants': [{'nick': 'TestUser', 'id': 1},
                               {'nick': 'User2', 'id': 2},
                               {'nick': 'User3', 'id': 3},
                               {'nick': 'User4', 'id': 4}],
              'subtasks': [{'subtask': "subtask_name", 'finished': False},
                           {'subtask': "subtask_name", 'finished': False},
                           {'subtask': "subtask_name", 'finished': False},
                           {'subtask': "subtask_name", 'finished': False},
                           {'subtask': "subtask_name", 'finished': False}],
              'start_time': 1710316871,
              'end_time': 1710316931
              }

    entry2 = {'hangout_name': 'Quiet murder',
              'duration': 180,
              "maker": {"username": "Raspberry Kitten", "discord_id": 1015276712948400148},
              'participants': [{'nick': 'Grey', 'id': 319472632493768705}],
              'subtasks': [{'subtask': "Go into your room", 'finished': True},
                           {'subtask': "Hide a camera in a bag of potato chips for some reason", 'finished': True},
                           {'subtask': "Take a potato chip", 'finished': True},
                           {'subtask': "Eat it", 'finished': True},
                           {'subtask': "Write someone's name down in your magic notebook", 'finished': False}],
              'start_time': 1710331781,
              'end_time': 1710331961
              }

    # Append both entries to a list
    entries = [entry1, entry2]

    # Write it to a file
    with open(test_database_name, 'w') as f:
        json.dump(entries, f)


def delete_test_file():
    if os.path.isfile(test_database_name):
        os.remove(test_database_name)
