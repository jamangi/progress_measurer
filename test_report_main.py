"""report_main gets called directly by the front-end file when the /start_entry command is used in Discord. This is a
function that flips all the given subtasks from False to True, then uses confirm_report to confirm that a subtask
'finished' value has been flipped to True, then creates a message to be sent to Discord."""

import pytest

from test_util import make_example_database, delete_test_file
from prog_backend import read_session, edit_value
from prog_cmds_and_funcs import report_main


@pytest.fixture(scope='session', autouse=True)
def setup_teardown():
    # Will be executed before the first test: create an example database to be used for testing
    make_example_database()
    yield 0
    # Will be executed after the last test: remove the example database
    delete_test_file()


def test_nothing_reported_error():
    """Test to make sure an error is raised if no subtasks are reported."""
    with pytest.raises(ValueError):
        report_main(filename=filename,
                    hangout_name='Quiet murder',
                    user_id=1015276712948400148)


def test_irrelevant_user_error():
    """Test to make sure an error is raised if the person who executed the slash command isn't one of the participants
    in ths hangout session being reported on."""
    with pytest.raises(ValueError):
        report_main(filename=filename,
                    hangout_name='Quiet murder',
                    user_id=1111111111111111111,
                    finished_subtask1='subtask5')


def test_repeated_subtask_error():
    """Test to make sure an error is raised if the same subtask is reported twice"""
    with pytest.raises(ValueError):
        report_main(filename=filename,
                    hangout_name='Sample Hangout',
                    user_id=1,
                    finished_subtask1='subtask1',
                    finished_subtask2='subtask1',
                    finished_subtask3='subtask3',
                    finished_subtask4='subtask4',
                    finished_subtask5='subtask5')
    with pytest.raises(ValueError):
        report_main(filename=filename,
                    hangout_name='Sample Hangout',
                    user_id=1,
                    finished_subtask1='subtask1',
                    finished_subtask2='subtask2',
                    finished_subtask3='subtask3',
                    finished_subtask4='subtask5',
                    finished_subtask5='subtask5')


def test_already_reported_error():
    """Test to make sure an error is raised if a subtask is reported complete when it's already listed as complete"""
    with pytest.raises(ValueError):
        report_main(filename=filename,
                    hangout_name='Quiet murder',
                    user_id=1015276712948400148,
                    finished_subtask1='subtask3')


def test_one_subtask_reported():
    """Runs report_main to make sure the 'finished' value was flipped to True, message is coming out right and
    there are no errors. In this test, we're reporting completion of subtask2 in Sample Hangout"""
    # Establish what we want the message to look like
    expected_message = (f"Report for Sample Hangout: the following objectives have been completed"
                        f"\n- subtask2"
                        f"\nSample Hangout is 20% complete!")

    # Run report_main, saving the string it returns as `message`
    message = report_main(filename, 'Sample Hangout', fin_task1="subtask2")

    # Check to make sure the 'finished' value was flipped to True
    results = read_session(filename, 'Sample Hangout')
    assert results['subtasks'][1]['finished'] is True

    # Check to make sure no other values were flipped to True
    assert all(subtask['finished'] is False for subtask in results['subtasks'] if subtask['subtask'] != 'subtask2')

    # Check to make sure the string that confirm_create_session returned matches exactly with the expected message
    assert message == expected_message

    # Teardown -- return the json to how it was before
    edit_value(filename, 'Sample Hangout', 'subtasks', False,
               subfield=1, subsubfield='finished')


def test_five_subtasks_reported():
    """Runs report_main to make sure the 'finished' values were flipped to True, message is coming out right and
    there are no errors. In this test, we're reporting completion of all subtasks in Sample Hangout"""
    # Establish what we want the message to look like
    expected_message = (f"Report for Sample Hangout: the following objectives have been completed"
                        f"\n- subtask1"
                        f"\n- subtask2"
                        f"\n- subtask3"
                        f"\n- subtask4"
                        f"\n- subtask5"
                        f"\nSample Hangout is 100% complete!")

    # Flip the desired subtasks to True
    edit_value(filename, 'Sample Hangout', 'subtasks', True,
               subfield=0, subsubfield='finished')
    edit_value(filename, 'Sample Hangout', 'subtasks', True,
               subfield=1, subsubfield='finished')
    edit_value(filename, 'Sample Hangout', 'subtasks', True,
               subfield=2, subsubfield='finished')
    edit_value(filename, 'Sample Hangout', 'subtasks', True,
               subfield=3, subsubfield='finished')
    edit_value(filename, 'Sample Hangout', 'subtasks', True,
               subfield=4, subsubfield='finished')

    # Run report_main, saving the string it returns as `message`
    message = report_main(filename, 'Sample Hangout',
                          fin_task1="subtask1",
                          fin_task2="subtask2",
                          fin_task3="subtask3",
                          fin_task4="subtask4",
                          fin_task5="subtask5")

    # Check to make sure the 'finished' values were all flipped to True
    results = read_session(filename, 'Sample Hangout')
    assert all([subtask['finished'] is True for subtask in results])

    # Check to make sure the string that confirm_create_session returned matches exactly with the expected message
    assert message == expected_message

    # Teardown -- return the json to how it was before
    edit_value(filename, 'Sample Hangout', 'subtasks', False,
               subfield=0, subsubfield='finished')
    edit_value(filename, 'Sample Hangout', 'subtasks', False,
               subfield=1, subsubfield='finished')
    edit_value(filename, 'Sample Hangout', 'subtasks', False,
               subfield=2, subsubfield='finished')
    edit_value(filename, 'Sample Hangout', 'subtasks', False,
               subfield=3, subsubfield='finished')
    edit_value(filename, 'Sample Hangout', 'subtasks', False,
               subfield=4, subsubfield='finished')


if __name__ == "__main__":
    pytest.main()
