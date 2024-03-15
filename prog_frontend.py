import os
from json import dump as json_dump
from decouple import config
from interactions import (SlashContext, OptionType, Client, listen,
                          SlashCommand, slash_option, AutocompleteContext)
import traceback
from interactions.api.events import CommandError

from prog_cmds_and_funcs import start_entry_main, report_main, history_main
from prog_backend import read_session
from prog_quickfetches import unreported_hangouts_quickfetch, completed_entries_quickfetch


@listen()
async def on_ready():
    """Lets the console know when the bot is online."""
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

    # Make sure the database file is already there. If it's not, create it
    if not os.path.isfile(config("FILENAME")) or not os.path.isfile(config("FILENAME")):
        with open(config("FILENAME"), 'w') as new_json:
            json_dump([], new_json)


@listen(CommandError, disable_default_listeners=True)  # tell the dispatcher that this replaces the default listener
async def on_command_error(event: CommandError):
    """Listens for any errors in slash commands. If an error is raised, this listener will catch it and store all the
    error messages in event.error. These errors are sent to the person who used the slash command as an ephemeral msg.

    :param event: (object) contains information about the interaction
    """
    traceback.print_exception(event.error)
    if not event.ctx.responded:
        errors = ''
        if event.error.args[0]:
            errors = '\nAlso! '.join(event.error.args)
        await event.ctx.send('Error! ' + errors, ephemeral=True)


base_command = SlashCommand(
    name="progress",
    description="For measuring our progress as we work on tasks.",
    scopes=[1126640506449973308, 1193614893870489720, 1199242556106612767])

# -------------------------------------------------------------------------------------------------------------------- #


@base_command.subcommand(sub_cmd_name="start_entry",
                         sub_cmd_description="Initiate a hangout session")
@slash_option(name="hangout_name", description="What will you call this hangout? 80 characters or less",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="duration", description="How many minutes will the hangout last?",
              opt_type=OptionType.NUMBER, required=True)
@slash_option(name="subtask1", description="Define a subtask for your hangout. 80 characters or less",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="subtask2", description="Define a subtask for your hangout. 80 characters or less",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="subtask3", description="Define a subtask for your hangout. 80 characters or less",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="subtask4", description="Define a subtask for your hangout. 80 characters or less",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="subtask5", description="Define a subtask for your hangout. 80 characters or less",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="participant2", description="Who, besides you, is participating?",
              opt_type=OptionType.USER, required=False)
@slash_option(name="participant3", description="Who, besides you, is participating?",
              opt_type=OptionType.USER, required=False)
@slash_option(name="participant4", description="Who, besides you, is participating?",
              opt_type=OptionType.USER, required=False)
async def start_entry(ctx: SlashContext, hangout_name, duration, subtask1, subtask2, subtask3, subtask4, subtask5,
                      participant2=None, participant3=None, participant4=None):
    """Start a hangout session with clearly defined goals.

    :param ctx: (object) contains information about the interaction
    :param hangout_name: (str) the name given to the session
    :param duration: (float) the number of minutes the session will last
    :param subtask1: (str) one of the subtasks that will be tackled in the session
    :param subtask2: (str) one of the subtasks that will be tackled in the session
    :param subtask3: (str) one of the subtasks that will be tackled in the session
    :param subtask4: (str) one of the subtasks that will be tackled in the session
    :param subtask5: (str) one of the subtasks that will be tackled in the session
    :param participant2: (user object) (optional) Discord info for another participant in the session
    :param participant3: (user object) (optional) Discord info for another participant in the session
    :param participant4: (user object) (optional) Discord info for another participant in the session
    """
    session_start_message = start_entry_main(filename=config('FILENAME'),
                                             hangout_name=hangout_name,
                                             duration=duration,
                                             maker=ctx.author,
                                             subtask1=subtask1,
                                             subtask2=subtask2,
                                             subtask3=subtask3,
                                             subtask4=subtask4,
                                             subtask5=subtask5,
                                             participant2=participant2,
                                             participant3=participant3,
                                             participant4=participant4,)
    # Send a message reporting the entry has been made and the session has been started
    await ctx.send(session_start_message)

# -------------------------------------------------------------------------------------------------------------------- #


@base_command.subcommand(sub_cmd_name="report",
                         sub_cmd_description="Report the results of a session")
@slash_option(name="hangout", description="Select which hangout session you'll be reporting on",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="finished_subtask1", description="A subtask that you want to report has been completed",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="finished_subtask2", description="A subtask that you want to report has been completed",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="finished_subtask3", description="A subtask that you want to report has been completed",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="finished_subtask4", description="A subtask that you want to report has been completed",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="finished_subtask5", description="A subtask that you want to report has been completed",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
async def report(ctx: SlashContext, hangout, finished_subtask1=None, finished_subtask2=None, finished_subtask3=None,
                 finished_subtask4=None, finished_subtask5=None):
    """Report on the results of a hangout session. How much of the goal you set out to accomplish actually got done?

    :param ctx: (object) contains information about the interaction
    :param hangout: (str) the name of the hangout session being reported on
    :param finished_subtask1: (str) the name of a subtask that is being reported as being finished
    :param finished_subtask2: (str) the name of a subtask that is being reported as being finished
    :param finished_subtask3: (str) the name of a subtask that is being reported as being finished
    :param finished_subtask4: (str) the name of a subtask that is being reported as being finished
    :param finished_subtask5: (str) the name of a subtask that is being reported as being finished
    """
    report_confirmation_message = report_main(filename=config("FILENAME"),
                                              hangout_name=hangout,
                                              user_id=int(ctx.author_id),
                                              finished_subtask1=finished_subtask1,
                                              finished_subtask2=finished_subtask2,
                                              finished_subtask3=finished_subtask3,
                                              finished_subtask4=finished_subtask4,
                                              finished_subtask5=finished_subtask5)
    # Send a message confirming that the report has been logged
    await ctx.send(report_confirmation_message)


@report.autocomplete("hangout")
async def report_hangoutsession_autocomplete(ctx: AutocompleteContext):
    """Fetches the list of all hangouts for a user to choose from if they want to report on them.

    :param ctx: (object) contains information about the interaction
    """
    # Fetch the list of unreported hangouts from the json. Make sure you respond within three seconds
    unreported_hangouts = unreported_hangouts_quickfetch(config("FILENAME"), int(ctx.author_id))
    await ctx.send(choices=unreported_hangouts)


@report.autocomplete("finished_subtask1")
@report.autocomplete("finished_subtask2")
@report.autocomplete("finished_subtask3")
@report.autocomplete("finished_subtask4")
@report.autocomplete("finished_subtask5")
async def report_subtask_autocomplete(ctx: AutocompleteContext):
    """Fetches the list of subtasks for a user to choose from the session that has been chosen. If no session has been
    chosen yet, this will not work.

    :param ctx: (object) contains information about the interaction
    """
    # Fetch the list of subtasks for the chosen session from the json. Make sure you respond within three seconds
    session_name = ctx.args[0]
    session_data = read_session(config("FILENAME"), session_name)
    subtasks_list = [{'name': subtask['subtask'], 'value': subtask['subtask']} for subtask in session_data['subtasks']]
    await ctx.send(choices=subtasks_list)


# @report.autocomplete("finished_subtask2")
# async def report_subtask1_autocomplete(ctx: AutocompleteContext):
#     """Fetches the list of subtasks for a user to choose from the session that has been chosen. If no session has been
#     chosen yet, this will not work.
#
#     :param ctx: (object) contains information about the interaction
#     """
#     # Fetch the list of subtasks for the chosen session from the json. Make sure you respond within three seconds
#     session_name = ctx.args[0]
#     session_data = read_session(config("FILENAME"), session_name)
#     subtasks_list = [{'name': subtask['subtask'], 'value': subtask['subtask']} for subtask in session_data['subtasks']]
#     await ctx.send(choices=subtasks_list)
#
#
# @report.autocomplete("finished_subtask3")
# async def report_subtask1_autocomplete(ctx: AutocompleteContext):
#     """Fetches the list of subtasks for a user to choose from the session that has been chosen. If no session has been
#     chosen yet, this will not work.
#
#     :param ctx: (object) contains information about the interaction
#     """
#     # Fetch the list of subtasks for the chosen session from the json. Make sure you respond within three seconds
#     session_name = ctx.args[0]
#     session_data = read_session(config("FILENAME"), session_name)
#     subtasks_list = [{'name': subtask['subtask'], 'value': subtask['subtask']} for subtask in session_data['subtasks']]
#     await ctx.send(choices=subtasks_list)
#
#
# @report.autocomplete("finished_subtask4")
# async def report_subtask_autocomplete(ctx: AutocompleteContext):
#     """Fetches the list of subtasks for a user to choose from the session that has been chosen. If no session has been
#     chosen yet, this will not work.
#
#     :param ctx: (object) contains information about the interaction
#     """
#     # Fetch the list of subtasks for the chosen session from the json. Make sure you respond within three seconds
#     session_name = ctx.args[0]
#     session_data = read_session(config("FILENAME"), session_name)
#     subtasks_list = [{'name': subtask['subtask'], 'value': subtask['subtask']} for subtask in session_data['subtasks']]
#     await ctx.send(choices=subtasks_list)
#
#
# @report.autocomplete("finished_subtask5")
# async def report_subtask1_autocomplete(ctx: AutocompleteContext):
#     """Fetches the list of subtasks for a user to choose from the session that has been chosen. If no session has been
#     chosen yet, this will not work.
#
#     :param ctx: (object) contains information about the interaction
#     """
#     # Fetch the list of subtasks for the chosen session from the json. Make sure you respond within three seconds
#     session_name = ctx.args[0]
#     session_data = read_session(config("FILENAME"), session_name)
#     subtasks_list = [{'name': subtask['subtask'], 'value': subtask['subtask']} for subtask in session_data['subtasks']]
#     await ctx.send(choices=subtasks_list)

# -------------------------------------------------------------------------------------------------------------------- #


@base_command.subcommand(sub_cmd_name="history",
                         sub_cmd_description="Get information about a past session")
@slash_option(name="hangout", description="Select which hangout session you want to know about",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
async def history(ctx: SlashContext, hangout):
    """Get information about a past hangout session.

    :param ctx: (object) contains information about the interaction
    :param hangout: (str) the name of the hangout session being investigated
    """
    history_report = history_main(filename=config("FILENAME"), hangout_name=hangout)
    # Send a message confirming that the report has been logged
    await ctx.send(history_report)


@history.autocomplete("hangout")
async def history_hangout_autocomplete(ctx: AutocompleteContext):
    """Fetches the list of complete entries for a user to choose from.

    :param ctx: (object) contains information about the interaction
    """
    # Fetch the list of completed entries from the json. Make sure you respond within three seconds
    completed_entries = completed_entries_quickfetch(config("FILENAME"))
    await ctx.send(choices=completed_entries)

# -------------------------------------------------------------------------------------------------------------------- #


if __name__ == "__main__":
    # Set the cwd to the directory where this file lives
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Define and start the bot
    bot = Client(token=config("BOT_TOKEN"))
    bot.start()

