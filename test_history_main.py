"""history_main is a function that reads an older session from the json and uses the info found there
to create a message to be sent to Discord."""

import pytest

from test_util import make_example_database, delete_test_file
from prog_cmds_and_funcs import history_main

filename = 'database_for_testing.json'


@pytest.fixture(scope='session', autouse=True)
def setup_teardown():
    # Will be executed before the first test: create an example database to be used for testing
    make_example_database()
    yield 0
    # Will be executed after the last test: remove the example database
    delete_test_file()


def test_quiet_murder():
    """Reads the session called "Quiet murder" and then makes sure the message that gets sent back from history_main
    is as it should be."""
    # Establish what we want the message to look like
    expected_message = (f"*Quiet murder*:"
                        f"Once upon a time (and that time was the 180 minutes between <t:1710331781:f> and "
                        f"<t:1710331961:t>), Raspberry Kitten and Grey hung out. Quiet murder was the objective, and "
                        f"to do that, here's what our busy bee(s) set out to do:"
                        f"\n- Go into your room -- which was finished"
                        f"\n- Hide a camera in a bag of potato chips for some reason -- which was finished"
                        f"\n- Take a potato chip -- which was finished"
                        f"\n- Eat it -- which was finished"
                        f"\n- Write someone's name down in your magic notebook -- which was NOT finished"
                        f"\nSo in total, there was a completion rate of 80%.")

    # Run confirm_history, saving the string it returns as `message`
    message = history_main(filename, 'Quiet murder')

    # Check to make sure the string that confirm_create_session returned matches exactly with the expected message
    assert message == expected_message


def test_sample_hangout():
    """Reads the session called "Sample Hangout" and then makes sure the message that gets sent back from history_main
    is as it should be."""
    # Establish what we want the message to look like
    expected_message = (f"*Sample Hangout*:"
                        f"Once upon a time (and that time was the 60 minutes between <t:1710316871:f> and "
                        f"<t:1710316931:t>), TestUser and User2 and User3 hung out. Sample Hangout was the "
                        f"objective, and to do that, here's what our busy bee(s) set out to do:"
                        f"\n- subtask1 -- which was NOT finished"
                        f"\n- subtask2 -- which was NOT finished"
                        f"\n- subtask3 -- which was NOT finished"
                        f"\n- subtask4 -- which was NOT finished"
                        f"\n- subtask5 -- which was NOT finished"
                        f"\nSo in total, there was a completion rate of 0%.")

    # Run confirm_history, saving the string it returns as `message`
    message = history_main(filename, 'Sample Hangout')

    # Check to make sure the string that confirm_create_session returned matches exactly with the expected message
    assert message == expected_message


if __name__ == "__main__":
    pytest.main()
