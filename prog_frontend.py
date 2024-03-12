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
@slash_option(name="duration", description="How many hours will the hangout last?",
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


if __name__ == "__main__":
    # Set the cwd to the directory where this file lives
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Define and start the bot
    bot = Client(token=config("BOT_TOKEN"))
    bot.start()

