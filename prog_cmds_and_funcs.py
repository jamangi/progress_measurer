from prog_backend import read_session, confirm_report, edit_value, create_session
from typing import Union, Dict, Any
import json
from datetime import datetime


def history_main(filename: str, hangout_name: str) -> str:
    """
    Read an older session from the JSON file and create a message to be sent to Discord.

    Args:
        filename (str): The name of the JSON file containing session data.
        hangout_name (str): The name of the hangout session to retrieve information for.

    Returns:
        str: A message summarizing the session.
    """
    # Read session data from the file
    session_data = read_session(filename, hangout_name)

    # Extract session information
    participants = [participant['nick'] for participant in session_data['participants']]
    participant_names = ' and '.join(participants)
    start_time = session_data['start_time']
    end_time = session_data['end_time']
    duration = session_data['duration']
    objective = session_data.get('objective', 'Objective information not available.')
    subtasks = session_data.get('subtasks', [])

    # Calculate completion rate
    completed_subtasks = [subtask for subtask in subtasks if subtask.get('finished', False)]
    completion_rate = len(completed_subtasks) / len(subtasks) * 100 if subtasks else 0

    # Format timestamps
    formatted_start_time = f"<t:{start_time}:f>"
    formatted_end_time = f"<t:{end_time}:t>"

    # Construct the message
    message = (
        f"*{hangout_name}*:"
        f"Once upon a time (and that time was the {duration} minutes between {formatted_start_time} and {formatted_end_time}), {participant_names} hung out. {hangout_name} was the "
        f"objective, and to do that, here's what our busy bee(s) set out to do:\n"
    )

    for subtask in subtasks:
        subtask_name = subtask.get('subtask', 'Unknown subtask')
        completion_status = "finished" if subtask.get('finished', False) else "NOT finished"
        message += f"- {subtask_name} -- which was {completion_status}\n"

    message += f"So in total, there was a completion rate of {completion_rate:.0f}%."
    return message

def start_entry_main(filename, hangout_name, duration, maker, subtask1, subtask2, subtask3, subtask4, subtask5, participant2=None, participant3=None, participant4=None ):
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
    create_session(filename, hangout_name, duration, maker, subtask1, subtask2,
                   subtask3, subtask4, subtask5, participant2, participant3, participant4)

    data = read_session(filename, hangout_name)

    # Generate message for Discord
    message = (f"A hangout session, {hangout_name}, has been started between "
               f"{' and '.join([p['nick'] for p in data['participants']])}. This session will last {duration} minutes, during which the following "
               f"five objectives should be completed:"
               f"\n- {subtask1}"
               f"\n- {subtask2}"
               f"\n- {subtask3}"
               f"\n- {subtask4}"
               f"\n- {subtask5}"
               f"\nDon't forget to report your achievements. Anchors aweigh!")

    return message

def report_main(filename: str, hangout_name: str, user_id: int, **finished_subtasks: Union[str, bool]) -> str:
    # Validate input parameters
    if not filename:
        raise ValueError("Filename cannot be empty.")
    if not hangout_name:
        raise ValueError("Hangout name cannot be empty.")
    if not isinstance(user_id, int):
        raise ValueError("User ID must be an integer.")
    if not finished_subtasks:
        raise ValueError("At least one subtask must be provided to report completion.")

    # Read session data from the file
    session_data = read_session(filename, hangout_name)

    # Check if the user is a participant in the hangout
    user_participant = next((participant for participant in session_data['participants'] if participant['discord_id'] == user_id), None)
    if user_participant is None:
        raise ValueError(f"User with ID {user_id} is not a participant in the hangout '{hangout_name}'.")

    # Update the status of the provided subtasks
    completed_subtasks = []
    for subtask_name, finished in finished_subtasks.items():
        subtask_index = next((index for index, subtask in enumerate(session_data['subtasks']) if subtask['subtask'] == subtask_name), None)
        if subtask_index is None:
            raise ValueError(f"Subtask '{subtask_name}' not found in the hangout '{hangout_name}'.")
        if session_data['subtasks'][subtask_index]['finished'] == finished:
            raise ValueError(f"Subtask '{subtask_name}' in the hangout '{hangout_name}' is already marked as {'finished' if finished else 'not finished'}.")
        session_data['subtasks'][subtask_index]['finished'] = finished
        if finished:
            completed_subtasks.append(subtask_name)

    # Save the updated session data
    edit_value(filename, hangout_name, 'subtasks', session_data['subtasks'])

    # Construct the message
    completion_rate = len(completed_subtasks) / len(session_data['subtasks']) * 100
    message = (
        f"Report for {hangout_name}: the following objectives have been completed\n"
        + ''.join(f'- {subtask}\n' for subtask in completed_subtasks)
        + f"{hangout_name} is {completion_rate:.0f}% complete!"
    )
    print(message)
    return message
