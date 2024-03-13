import json
from datetime import datetime


def create_session(filename, hangout_name, duration, maker, participant2, participant3, participant4, subtask1,
                   subtask2, subtask3, subtask4, subtask5=None):
    participants = [maker, participant2, participant3, participant4]
    subtasks = [subtask1, subtask2, subtask3, subtask4]
    if subtask5 is not None:
        subtasks.append(subtask5)

    session_data = {
        "hangout_name": hangout_name,
        "duration": duration,
        "participants": [
            {"username": participant.username, "discord_id": participant.id, "display_name": participant.display_name}
            for participant in participants
        ],
        "subtasks": [{"subtask": task, "finished": False} for task in subtasks if task is not None],
        "start_time": int(datetime.now().timestamp()),
        "end_time": None
    }

