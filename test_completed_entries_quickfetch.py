import pytest

from test_util import make_example_database, delete_test_file
from prog_backend import edit_value

from prog_quickfetches import completed_entries_quickfetch


filename = 'database_for_testing.json'


@pytest.fixture(scope='session', autouse=True)
def setup_teardown():
    # Will be executed before the first test: create an example database to be used for testing
    make_example_database()
    yield 0
    # Will be executed after the last test: remove the example database
    delete_test_file()


def test_quiet_murder():
    """Test to make sure the output is as expected for a participant in Quiet muirder but not Sample Hangout.
    The returned list should include only Quiet murder."""
    expected_list = [{'name': 'Quiet murder', 'value': 'Quiet murder'}]
    test_list = completed_entries_quickfetch(filename)
    assert test_list == expected_list


def test_two_entries():
    """Test to make sure the output is as expected when the there are two valid reported-on hangout sessions on record.
    To this end, subtask1 in Sample Hangout will be flipped to True."""
    expected_list = [{'name': 'Sample Hangout', 'value': 'Sample Hangout'},
                     {'name': 'Quiet murder', 'value': 'Quiet murder'}]
    edit_value(filename, 'Sample Hangout', 'subtasks', True, 0, 'finished')
    test_list = completed_entries_quickfetch(filename)
    assert test_list == expected_list


if __name__ == "__main__":
    pytest.main()
