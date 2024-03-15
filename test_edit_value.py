import pytest

from test_util import make_example_database, delete_test_file
from prog_backend import edit_value, read_session

filename = 'database_for_testing.json'


@pytest.fixture(scope='session', autouse=True)
def setup_teardown():
    # Will be executed before the first test: create an example database to be used for testing
    make_example_database()
    yield 0
    # Will be executed after the last test: remove the example database
    delete_test_file()


def test_finish_subtask():
    """Change a subtask's 'finished' status to True to reflect that it's been finished"""
    expected_value = True
    edit_value(filename=filename, session_name='Sample Hangout', field='subtasks', new_value=True, subfield=3,
               subsubfield='finished')
    results = read_session(filename, 'Sample Hangout')
    test_value = results['subtasks'][3]['finished']
    assert test_value == expected_value


def test_unfinish_subtask():
    """Change a subtask's 'finished' status into False to reflect that it actually hadn't been finished"""
    expected_value = False
    edit_value(filename=filename, session_name='Quiet murder', field='subtasks', new_value=False, subfield=1,
               subsubfield='finished')
    results = read_session(filename, 'Quiet murder')
    test_value = results['subtasks'][1]['finished']
    assert test_value == expected_value


def test_change_duration():
    """Try changing the duration of the session called Sample Hangout"""
    expected_duration = 400
    edit_value(filename=filename, session_name='Sample Hangout', field="duration", new_value=400)
    results = read_session(filename, 'Sample Hangout')
    test_duration = results['duration']
    start_time = results['start_time']
    test_end_time = results['end_time']
    expected_end_time = start_time + expected_duration*60
    assert test_duration == expected_duration
    assert test_end_time == expected_end_time


def test_remove_participant():
    """Try removing a participant from the participants list in Quiet murder"""
    expected_participants = [{'nick': 'Raspberry Kitten', 'discord_id': 1015276712948400148}]
    removed_participant = {'nick': 'Grey', 'discord_id': 319472632493768705}
    edit_value(filename=filename, session_name='Quiet murder', field="participants", new_value=removed_participant,
               change='remove')
    results = read_session(filename, 'Quiet murder')
    test_participants = [participant for participant in results['participants']]
    assert all([participant in test_participants for participant in expected_participants])
    assert removed_participant not in test_participants
    assert len(expected_participants) == len(test_participants)


def test_add_participant():
    """Try adding a participant to the participants list in Sample Hangout"""
    expected_participants = [{'nick': 'TestUser', 'discord_id': 1},
                             {'nick': 'User2', 'discord_id': 2},
                             {'nick': 'User3', 'discord_id': 3},
                             {'nick': 'Anytime', 'discord_id': 309330832047210497}]
    added_participant = {'nick': 'Anytime', 'discord_id': 309330832047210497}
    edit_value(filename=filename, session_name='Sample Hangout', field="participants", new_value=added_participant,
               change='add')
    results = read_session(filename, 'Sample Hangout')
    test_participants = [participant for participant in results['participants']]
    assert all([participant in test_participants for participant in expected_participants])
    assert added_participant in test_participants
    assert len(expected_participants) == len(test_participants)


def test_change_start_time():
    """Try changing the starting time of the session called Sample Hangout"""
    expected_start_time = 171031700
    edit_value(filename=filename, session_name='Sample Hangout', field="start_time", new_value=171031700)
    results = read_session(filename, 'Sample Hangout')
    test_start_time = results['start_time']
    duration = results['duration']
    test_end_time = results['end_time']
    expected_end_time = expected_start_time + duration*60
    assert test_start_time == expected_start_time
    assert test_end_time == expected_end_time


def test_change_hangout_name():
    """Try changing the name of the session called Sample Hangout"""
    expected_value = "Sit on a cactus"
    edit_value(filename=filename, session_name='Sample Hangout', field="hangout_name", new_value="Sit on a cactus")
    test_value = read_session(filename, 'Sit on a cactus')['hangout_name']
    assert test_value == expected_value


if __name__ == "__main__":
    pytest.main()
