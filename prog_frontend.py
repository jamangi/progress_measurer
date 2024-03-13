import os
from decouple import config
from interactions import (SlashContext, OptionType, Client, listen,
                          SlashCommand, slash_option, AutocompleteContext)
import traceback
from interactions.api.events import CommandError


@listen()
async def on_ready():
    """Lets the console know when the bot is online."""
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


# @listen(CommandError, disable_default_listeners=True)  # tell the dispatcher that this replaces the default listener
# async def on_command_error(event: CommandError):
#     """Listens for any errors in slash commands. If an error is raised, this listener will catch it and store all the
#     error messages in event.error. These errors are sent to the person who used the slash command as an ephemeral msg.
#
#     :param event: (object) contains information about the interaction
#     """
#     traceback.print_exception(event.error)
#     if not event.ctx.responded:
#         errors = ''
#         if event.error.args[0]:
#             errors = '\nAlso! '.join(event.error.args)
#         await event.ctx.send('Error! ' + errors, ephemeral=True)


base_command = SlashCommand(
    name="progress",
    description="For measuring our progress as we work on tasks.",
    scopes=[1126640506449973308, 1193614893870489720, 1199242556106612767])


@base_command.subcommand(sub_cmd_name="start_entry",
                         sub_cmd_description="Initiate a hangout session")
@slash_option(name="hangout_name", description="What will you call this hangout? 99 characters or less",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="duration", description="How many minutes will the hangout last?",
              opt_type=OptionType.NUMBER, required=True)
@slash_option(name="subtask1", description="Define a subtask for your hangout",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="subtask2", description="Define a subtask for your hangout",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="subtask3", description="Define a subtask for your hangout",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="subtask4", description="Define a subtask for your hangout",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="subtask5", description="Define a subtask for your hangout",
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
    :param hangout_name:
    :param duration:
    :param participant2:
    :param participant3:
    :param participant4:
    :param subtask1:
    :param subtask2:
    :param subtask3:
    :param subtask4:
    :param subtask5:
    """
    session_start_message = start_entry_main(hangout_name=hangout_name,
                                             duration=duration,
                                             maker=ctx.author,
                                             participant2=participant2,
                                             participant3=participant3,
                                             participant4=participant4,
                                             subtask1=subtask1,
                                             subtask2=subtask2,
                                             subtask3=subtask3,
                                             subtask4=subtask4,
                                             subtask5=subtask5)
    # Send a message reporting the entry has been made and the session has been started
    await ctx.send(session_start_message)


@base_command.subcommand(sub_cmd_name="report",
                         sub_cmd_description="Report the results of a session")
@slash_option(name="entry", description="Select which session you'll be reporting on",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="completion", description="What percentage of the tasks that were set out to do were completed?",
              opt_type=OptionType.NUMBER, required=True)
@slash_option(name="comment", description="Any additional comments?",
              opt_type=OptionType.STRING, required=False)
async def report(ctx: SlashContext, entry, completion, comment=None):
    """Report on the results of a session. How much of the goal you set out to accomplish actually got done?

    :param ctx: (object) contains information about the interaction
    :param entry:
    :param completion:
    :param comment:
    """
    report_confirmation_message = report_main(entry_name=entry,
                                              user_id=int(ctx.author_id),
                                              completion=completion,
                                              comment=comment)
    # Send a message confirming that the report has been logged
    await ctx.send(report_confirmation_message)


@report.autocomplete("entry")
async def report_autocomplete(ctx: AutocompleteContext):
    """Fetches the list of incomplete reports for a user to choose from

    :param ctx: (object) contains information about the interaction
    """
    # Fetch the list of reports from the json. Make sure you respond within three seconds
    unreported_entries = unreported_entries_quickfetch(int(ctx.author_id))
    await ctx.send(choices=unreported_entries)


@base_command.subcommand(sub_cmd_name="history",
                         sub_cmd_description="Get information about a past session")
@slash_option(name="entry", description="Select which session you want to know about",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
async def history(ctx: SlashContext, entry):
    """Get information about a past session.

    :param ctx: (object) contains information about the interaction
    :param entry:
    """
    history_report = history_main(entry_name=entry)
    # Send a message confirming that the report has been logged
    await ctx.send(history_report)


@history.autocomplete("entry")
async def report_autocomplete(ctx: AutocompleteContext):
    """Fetches the list of complete entries for a user to choose from

    :param ctx: (object) contains information about the interaction
    """
    # Fetch the list of completed entries from the json. Make sure you respond within three seconds
    completed_entries = completed_entries_quickfetch(int(ctx.author_id))
    await ctx.send(choices=completed_entries)


if __name__ == "__main__":
    # Set the cwd to the directory where this file lives
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Define and start the bot
    bot = Client(token=config("BOT_TOKEN"))
    bot.start()

