from prog_backend import read_session

def history_main(filename: str, hangout_name: str) -> str:
    session_data = read_session(filename, hangout_name)
 message = (
        f"Once upon a time (and that time was the 180 minutes between {start_time} and "
        f"{end_time}, {participant_list} hung out. {hangout_name} was the objective, and"
        f"to do that, here's what our busy bee(s) set out to do:"
        f"- {chr(10).join(subtasks)}\n"
        f"So in total, therecompletion{int(percentage)}% complete!"
    )