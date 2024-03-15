import pytest

from test_util import make_example_database, delete_test_file
from prog_backend import create_session

from prog_quickfetches import unreported_hangouts_quickfetch


filename = 'database_for_testing.json'


class EmptyUser:
    def __init__(self, display_name=None, username=None, user_id=None):
        self.display_name = display_name
        self.username = username
        self.id = user_id


User1 = EmptyUser('User1', 'userthefirst', 1)
User2 = EmptyUser('User2', 'userthesecond', 2)


@pytest.fixture(scope='session', autouse=True)
def setup_teardown():
    # Will be executed before the first test: create an example database to be used for testing
    make_example_database()
    yield 0
    # Will be executed after the last test: remove the example database
    delete_test_file()


def test_sample_hangout():
    """Test to make sure the output is as expected for a participant in Sample Hangout but not Quiet murder.
    The returned list should include only Sample Hangout."""
    expected_list = [{'name': 'Sample Hangout', 'value': 'Sample Hangout'}]
    test_list = unreported_hangouts_quickfetch(filename, 1)
    assert test_list == expected_list


def test_quiet_murder_reported():
    """Test to make sure the output is as expected for a participant in Quiet murder but not Sample Hangout.
    Quiet murder has four subtasks already flipped to True, so the returned list should be empty."""
    expected_list = []
    test_list = unreported_hangouts_quickfetch(filename, 319472632493768705)
    assert test_list == expected_list


def test_two_entries():
    """Test to make sure the output is as expected when the user is a participant in two different unreported hangouts.
    To this end, a new hangout is added to the json before the test begins."""
    expected_list = [{'name': 'Sample Hangout', 'value': 'Sample Hangout'},
                     {'name': 'session for testing', 'value': 'session for testing'}]
    create_session(filename, 'session for testing', 100, User2,
                   '1', '2', '3', '4', '5', User1)
    test_list = unreported_hangouts_quickfetch(filename, 2)
    assert test_list == expected_list

if __name__ == "__main__":
    pytest.main()
