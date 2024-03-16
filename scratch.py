from test_util import make_example_database
from prog_backend import edit_value, read_session, confirm_report
make_example_database()
filename = 'database_for_testing.json'
"""
expected_participants = [{'nick': 'Raspberry Kitten', 'discord_id': 1015276712948400148}]
removed_participant = {'nick': 'Grey', 'discord_id': 319472632493768705}
edit_value(filename=filename, session_name='Quiet murder', field="participants", new_value=removed_participant,
               change='remove')
results = read_session(filename, 'Quiet murder')
test_participants = [participant for participant in results['participants']]
assert all([participant in test_participants for participant in expected_participants])
assert removed_participant not in test_participants
assert len(expected_participants) == len(test_participants)"""

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

confirm_report(filename,"Sample Hangout",**kwarg)
history_main(filename, hangout_name)