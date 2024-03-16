from prog_backend import read_session, confirm_report, edit_value
from typing import Union
import json
from datetime import datetime

def history_main(filename: str, hangout_name: str) -> str:
    session_data = read_session(filename, hangout_name)

    participants = [participant['nick'] for participant in session_data['participants']]
    participant_names = ' and '.join(participants)

    start_time = session_data['start_time']
    end_time = session_data['end_time']
    duration = session_data['duration']

    objective = session_data.get('objective', 'Objective information not available.')

    subtasks = session_data.get('subtasks', [])
    completed_subtasks = [subtask for subtask in subtasks if subtask.get('finished', True)]
    completion_rate = len(completed_subtasks) / len(subtasks) * 100 if subtasks else 0

    formatted_start_time = f"<t:{start_time}:f>"
    formatted_end_time = f"<t:{end_time}:t>"

    message = (
        f"*{hangout_name}*:\n"
        f"Once upon a time (and that time was the {duration} minutes between {formatted_start_time} and {formatted_end_time}), {participant_names} hung out. {objective} was the "
        f"objective, and to do that, here's what our busy bee(s) set out to do:\n"
    )

    for subtask in subtasks:
        subtask_name = subtask.get('name', 'Unknown subtask')
        completion_status = "finished" if subtask.get('finished', False) else "NOT finished"
        message += f"- {subtask_name} -- which was {completion_status}\n"

    message += f"So in total, there was a completion rate of {completion_rate:.0f}%."
    print(message)
    return message

def start_entry_main(filename, hangout_name, duration, maker, subtask1, subtask2, subtask3, subtask4, subtask5, participant2):
    # Validate input parameters
    if len(hangout_name) > 80:
        raise ValueError("Hangout name is too long")
    if len(subtask1) > 80 or len(subtask2) > 80 or len(subtask3) > 80 or len(subtask4) > 80 or len(subtask5) > 80:
        raise ValueError("Subtask name is too long")
    if maker.id == participant2.id:
        raise ValueError("Maker cannot be among the participants")
    if duration > 1440:
        raise ValueError("Duration cannot be greater than one day")

    # Create hangout session data
    session_data = {
        "hangout_name": hangout_name,
        "duration": duration,
        "maker": {
            "display_name": maker.display_name,
            "username": maker.username,
            "id": maker.id
        },
        "participant2": {
            "display_name": participant2.display_name,
            "username": participant2.username,
            "id": participant2.id
        },
        "subtasks": [subtask1, subtask2, subtask3, subtask4, subtask5],
        "start_time": int(datetime.now().timestamp()),
        "end_time": None  # To be updated later
    }

    # Write session data to JSON file
    with open(filename, 'w') as file:
        json.dump([session_data], file, indent=4)

    # Generate message for Discord
    message = (f"A hangout session, {hangout_name}, has been started between {maker.display_name} and "
               f"{participant2.display_name}. This session will last {duration} minutes, during which the following "
               f"five objectives should be completed:\n"
               f"\n- {subtask1}"
               f"\n- {subtask2}"
               f"\n- {subtask3}"
               f"\n- {subtask4}"
               f"\n- {subtask5}"
               f"\nDon't forget to report your achievements. Anchors aweigh!")

    return message

def report_main(filename: str, hangout_name: str, user_id: int, **finished_subtasks: Union[str, bool]) -> str:
    session_data = read_session(filename, hangout_name)

    # Check if the user is a participant in the hangout
    user_participant = next((participant for participant in session_data['participants'] if participant['discord_id'] == user_id), None)
    if user_participant is None:
        raise ValueError(f"User with ID {user_id} is not a participant in the hangout '{hangout_name}'.")

    # Check if any subtasks are provided to be marked as finished
    if not finished_subtasks:
        raise ValueError("At least one subtask must be provided to report completion.")

    # Check if any subtasks have already been marked as finished
    for subtask_name, finished in finished_subtasks.items():
        subtask_index = next((index for index, subtask in enumerate(session_data['subtasks']) if subtask['subtask'] == subtask_name), None)
        if subtask_index is None:
            raise ValueError(f"Subtask '{subtask_name}' not found in the hangout '{hangout_name}'.")
        if session_data['subtasks'][subtask_index]['finished'] == finished:
            raise ValueError(f"Subtask '{subtask_name}' in the hangout '{hangout_name}' is already marked as {'finished' if finished else 'not finished'}.")

    # Update the 'finished' status of the provided subtasks
    for subtask_name, finished in finished_subtasks.items():
        subtask_index = next((index for index, subtask in enumerate(session_data['subtasks']) if subtask['name'] == subtask_name), None)
        session_data['subtasks'][subtask_index]['finished'] = finished

    # Save the updated session data
    edit_value(filename, hangout_name, 'subtasks', session_data['subtasks'])

    # Construct the message
    completed_subtasks = [subtask_name for subtask_name, finished in finished_subtasks.items() if finished]
    completion_rate = len(completed_subtasks) / len(session_data['subtasks']) * 100
    message = (
            f"Report for {hangout_name}: the following objectives have been completed\n"
            + ''.join(f'- {subtask}' + '\n' for subtask in completed_subtasks)
            + f"{hangout_name} is {completion_rate:.0f}% complete!"
    )
    print(message)
    return message
#test