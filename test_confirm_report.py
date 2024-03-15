"""confirm_report is a function that reads to confirm that a subtask 'finished' value has been flipped to True, then
creates a message to be sent to Discord."""

import pytest

from test_util import make_example_database, delete_test_file
from prog_backend import confirm_report, edit_value

filename = 'database_for_testing.json'


@pytest.fixture(scope='session', autouse=True)
def setup_teardown():
    # Will be executed before the first test: create an example database to be used for testing
    make_example_database()
    yield 0
    # Will be executed after the last test: remove the example database
    delete_test_file()


def test_one_subtask_reported():
    """Flips the desired subtask to True, then runs confirm_report to make sure the message is coming out right and
    there are no errors."""
    # Establish what we want the message to look like
    expected_message = (f"Report for Sample Hangout: the following objectives have been completed"
                        f"\n- subtask2"
                        f"\nSample Hangout is 20% complete!")

    # Flip the desired subtask to True
    edit_value(filename, 'Sample Hangout', 'subtasks', True,
               subfield=1, subsubfield='finished')

    # Run confirm_create_sesssion, saving the string it returns as `message`
    message = confirm_report(filename, 'Sample Hangout', fin_task1="subtask2")

    # Check to make sure the string that confirm_create_session returned matches exactly with the expected message
    assert message == expected_message

    # Teardown -- return the json to how it was before
    edit_value(filename, 'Sample Hangout', 'subtasks', False,
               subfield=1, subsubfield='finished')


def test_five_subtasks_reported():
    """Flips the all subtasks to True, then runs confirm_report to make sure the message is coming out right and
    there are no errors."""
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

    # Run confirm_create_sesssion, saving the string it returns as `message`
    message = confirm_report(filename, 'Sample Hangout',
                             fin_task1="subtask1",
                             fin_task2="subtask2",
                             fin_task3="subtask3",
                             fin_task4="subtask4",
                             fin_task5="subtask5")

    # Check to make sure the string that confirm_create_session returned matches exactly with the expected message
    assert message == expected_message


def test_not_flipped_error():
    """Checks to make sure an exception shows up in the unlikely event that the value hasn't been flipped to True"""
    with pytest.raises(ValueError, match="The subtask that was supposed to be reported has not been recorded as "
                                         "finished. This is probably an issue with the code. The data file may "
                                         "be compromised. Do not use any more commands and immediately investigate "
                                         "or contact someone familiar with the code."):
        edit_value(filename, 'Quiet murder', 'subtasks', False,
                   subfield=4, subsubfield='finished')
        confirm_report(filename, 'Sample Hangout', fin_task1="Write someone's name down in your magic notebook")


if __name__ == "__main__":
    pytest.main()
