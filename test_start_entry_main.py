"""start_entry_main gets called directly by the front-end file when the /start_entry command is used in Discord. This
function is used to create a new hangout session that starts immediately and store it in the json file. It then sends
a message to Discord announcing that it worked."""

import pytest
import os
import json
from datetime import datetime

from test_util import make_example_database, delete_test_file
from prog_cmds_and_funcs import start_entry_main

filename = 'database_for_testing.json'


class EmptyUser:
    def __init__(self, display_name=None, username=None, user_id=None):
        self.display_name = display_name
        self.username = username
        self.id = user_id


Kat = EmptyUser('Kat', 'dorkiedeer', 583730259409633310)
Posi = EmptyUser('Anytime', 'mr.positions', 309330832047210497)


@pytest.fixture(scope='session', autouse=True)
def setup_teardown():
    # Will be executed before the first test: create an example database to be used for testing
    make_example_database()
    yield 0
    # Will be executed after the last test: remove the example database
    delete_test_file()


def test_name_too_long_error():
    """Tests to make sure an exception is raised if the hangout name is over 80 characters, but not if it's under 80."""
    # Make sure super long names are out of the question
    with pytest.raises(ValueError):
        start_entry_main(filename=filename,
                         hangout_name='99 bottles of beer on the wall, 99 bottles of beer; take one down, pass it '
                                      'around, 98 bottles of beer on the wall. Hopefully that is more than 100 '
                                      'characters because I do not really want to type more than that',
                         duration=125,
                         maker=Kat,
                         subtask1='Go to the kitchen',
                         subtask2='Open the fridge',
                         subtask3='Take a bag of salad mix',
                         subtask4='Eat it',
                         subtask5='Spit out the plastic',
                         participant2=Posi)

    # Make sure 81 characters are out of the question, also
    with pytest.raises(ValueError):
        start_entry_main(filename=filename,
                         hangout_name='99 bottles of beer on the wall, 99 bottles of beer; '
                                      'take one down, pass it around',
                         duration=125,
                         maker=Kat,
                         subtask1='Go to the kitchen',
                         subtask2='Open the fridge',
                         subtask3='Take a bag of salad mix',
                         subtask4='Eat it',
                         subtask5='Spit out the plastic',
                         participant2=Posi)

    # Finally, make sure if it has 80 characters it passes successfully
    start_entry_main(filename=filename,
                     hangout_name='99 bottles of beer on the wall, 99 bottles of beer; '
                                  'take one down, pass it round',
                     duration=125,
                     maker=Kat,
                     subtask1='Go to the kitchen',
                     subtask2='Open the fridge',
                     subtask3='Take a bag of salad mix',
                     subtask4='Eat it',
                     subtask5='Spit out the plastic',
                     participant2=Posi)


def test_subtasks_too_long_error():
    """Tests to make sure an exception is raised if any of the subtasks are over 80 characters, but not if they're
    all under 80 characters."""
    # Try for an error when subtask1 is too long
    with pytest.raises(ValueError):
        start_entry_main(filename=filename,
                         hangout_name='subtask1 81 characters',
                         duration=300,
                         maker=Kat,
                         subtask1='a'*81,
                         subtask2='b'*80,
                         subtask3='c'*80,
                         subtask4='d'*80,
                         subtask5='e'*80,
                         participant2=Posi)

    # Try for an error when subtask2 is too long
    with pytest.raises(ValueError):
        start_entry_main(filename=filename,
                         hangout_name='subtask2 81 characters',
                         duration=300,
                         maker=Kat,
                         subtask1='a'*80,
                         subtask2='b'*81,
                         subtask3='c'*80,
                         subtask4='d'*80,
                         subtask5='e'*80,
                         participant2=Posi)

    # Try for an error when subtask3 is too long
    with pytest.raises(ValueError):
        start_entry_main(filename=filename,
                         hangout_name='subtask3 81 characters',
                         duration=300,
                         maker=Kat,
                         subtask1='a'*80,
                         subtask2='b'*80,
                         subtask3='c'*81,
                         subtask4='d'*80,
                         subtask5='e'*80,
                         participant2=Posi)

    # Try for an error when subtask4 is too long
    with pytest.raises(ValueError):
        start_entry_main(filename=filename,
                         hangout_name='subtask4 81 characters',
                         duration=300,
                         maker=Kat,
                         subtask1='a'*80,
                         subtask2='b'*80,
                         subtask3='c'*80,
                         subtask4='d'*81,
                         subtask5='e'*80,
                         participant2=Posi)

    # Try for an error when subtask5 is too long
    with pytest.raises(ValueError):
        start_entry_main(filename=filename,
                         hangout_name='subtask5 81 characters',
                         duration=300,
                         maker=Kat,
                         subtask1='a'*80,
                         subtask2='b'*80,
                         subtask3='c'*80,
                         subtask4='d'*80,
                         subtask5='e'*81,
                         participant2=Posi)


def test_self_among_participants_error():
    """Tests to make sure an exception is raised if the maker is also submitted as one of the participants."""
    with pytest.raises(ValueError):
        start_entry_main(filename=filename,
                         hangout_name='99 bottles of beer on the wall, 99 bottles of beer; '
                                      'take one down, pass it around',
                         duration=125,
                         maker=Kat,
                         subtask1='Go to the kitchen',
                         subtask2='Open the fridge',
                         subtask3='Take a bag of salad mix',
                         subtask4='Eat it',
                         subtask5='Spit out the plastic',
                         participant2=Kat)


def test_duration_over_one_day_error():
    """Tests to make sure an exception is raised if the duration submitted is greater than 1440 minutes (one day)."""
    # Make sure super long durations are out of the question
    with pytest.raises(ValueError):
        start_entry_main(filename=filename,
                         hangout_name='100000 duration test',
                         duration=100000,
                         maker=Kat,
                         subtask1='Go to the kitchen',
                         subtask2='Open the fridge',
                         subtask3='Take a bag of salad mix',
                         subtask4='Eat it',
                         subtask5='Spit out the plastic',
                         participant2=Posi)

    # Make sure a duration of 1441 is out of the question, also
    with pytest.raises(ValueError):
        start_entry_main(filename=filename,
                         hangout_name='1441 test',
                         duration=1441,
                         maker=Kat,
                         subtask1='Go to the kitchen',
                         subtask2='Open the fridge',
                         subtask3='Take a bag of salad mix',
                         subtask4='Eat it',
                         subtask5='Spit out the plastic',
                         participant2=Posi)

    # Finally, make sure if duration == 1440 it passes successfully
    start_entry_main(filename=filename,
                     hangout_name='1440 test',
                     duration=1440,
                     maker=Kat,
                     subtask1='Go to the kitchen',
                     subtask2='Open the fridge',
                     subtask3='Take a bag of salad mix',
                     subtask4='Eat it',
                     subtask5='Spit out the plastic',
                     participant2=Posi)


def test_create_json():
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

    start_entry_main(**data1)  # requires keyword args

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


def test_get_message():
    """Creates a session called "Eat vegetables" and then makes sure the result from confirm_create_session is a
    message with the expected format and information"""
    # Establish what we want the message to look like
    expected_message = (f"A hangout session, Eat vegetables, has been started between Kat and Anytime. This "
                        f"session will last 125 minutes, during which the following five objectives should be "
                        f"completed:"
                        f"\n- Go to the kitchen"
                        f"\n- Open the fridge"
                        f"\n- Take a bag of salad mix"
                        f"\n- Eat it"
                        f"\n- Spit out the plastic"
                        f"\nDon't forget to report your achievements. Anchors aweigh!")

    # Run start_entry_main, saving the string it returns as `message`
    message = start_entry_main(filename=filename,
                               hangout_name='Eat vegetables',
                               duration=125,
                               maker=Kat,
                               subtask1='Go to the kitchen',
                               subtask2='Open the fridge',
                               subtask3='Take a bag of salad mix',
                               subtask4='Eat it',
                               subtask5='Spit out the plastic',
                               participant2=Posi)

    # Check to make sure the string that confirm_create_session returned matches exactly with the expected message
    assert message == expected_message


if __name__ == "__main__":
    pytest.main()
