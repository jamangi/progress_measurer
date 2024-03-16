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

make_example_database()

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
print(message)
print()
print(expected_message)
assert message == expected_message