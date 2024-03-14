"""confirm_create_session is a function that reads a newly created session from the json and uses the info found there
to create a message to be sent to Discord."""

import pytest

from test_util import make_example_database, delete_test_file
from prog_backend import confirm_create_session, create_session

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


def test_get_message():
    """Creates a session called "Eat vegetables" and then makes sure the result from confirm_create_session is a
    message with the expected format and information"""
    # Establish what we want the message to look like
    expected_message = (f"A hangout session, Eat vegetables, has been started between Kat and Posi. This "
                        f"session will last 125 minutes, during which the following five objectives should be "
                        f"completed:"
                        f"\n- Go to the kitchen"
                        f"\n- Open the fridge"
                        f"\n- Take a bag of salad mix"
                        f"\n- Eat it"
                        f"\n- Spit out the plastic"
                        f"\nDon't forget to report your achievements. Anchors aweigh!")

    # Make a new session entry called Eat vegetables
    create_session(filename, 'Eat vegetables', 125, Kat, 'Go to the kitchen',
                   'Open the fridge', 'Take a bag of salad mix', 'Eat it',
                   'Spit out the plastic', participant2=Posi)

    # Run confirm_create_sesssion, saving the string it returns as `message`
    message = confirm_create_session(filename, 'Eat vegetables')

    # Check to make sure the string that confirm_create_session returned matches exactly with the expected message
    assert message == expected_message


if __name__ == "__main__":
    pytest.main()
