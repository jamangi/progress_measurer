from prog_backend import read_session, confirm_report
import json

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

def start_entry_main():
    pass

def report_main(filename, hangout_name, user_id):
    pass