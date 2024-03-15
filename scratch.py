from test_util import make_example_database
from prog_backend import edit_value, read_session, confirm_report
"""make_example_database()
filename = 'database_for_testing.json'

expected_participants = [{'nick': 'Raspberry Kitten', 'discord_id': 1015276712948400148}]
removed_participant = {'nick': 'Grey', 'discord_id': 319472632493768705}
edit_value(filename=filename, session_name='Quiet murder', field="participants", new_value=removed_participant,
               change='remove')
results = read_session(filename, 'Quiet murder')
test_participants = [participant for participant in results['participants']]
assert all([participant in test_participants for participant in expected_participants])
assert removed_participant not in test_participants
assert len(expected_participants) == len(test_participants)"""

confirm_report(filename:str,hangout_name:str, **kwargs) -> str