import argparse
import sys
import re
import time
import os

from slackclient import SlackClient

from substack.data.profile import Profile
from substack.substack_core import SubStack
from substack.data.profile import Profile
from substack.substack_core import SubStack
from substack.data.notifier import Notifier

BOT_NAME = 'substack'


def get_slack_id():
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                return user.get('id')
    else:
        raise Exception, "could not find bot user with the name " + BOT_NAME


SLACKBOT_ID = get_slack_id()


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:

            if output and 'text' in output and 'channel' in output and 'user' in output \
                and output['type'] == 'message' and output['user'] != SLACKBOT_ID \
                    and "<@{}>".format(SLACKBOT_ID) in output['text']:
                message = output['text'].strip()
                message = message.replace("<@{}>".format(SLACKBOT_ID), '').strip().lower()
                return message, \
                       output['channel']
    return None, None


def handle_command(command):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    if command.startswith("check") or command.startswith("scan"):
        command = command.strip().lower()

        if command.count(' ') < 1:
            notifier = Notifier()
            notifier.send_slack("Hi, please specific your command. eg: `scan example.com`")
            return

    domain_list = re.findall(r"\|([\w\.]*\.\w*)\>", command)

    for domain in domain_list:
        profile = Profile("empty")
        profile.set_target(domain)

        sub_stack = SubStack()
        sub_stack.set_profile(profile)

        sub_stack.start()


if __name__ == '__main__':
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    notifier = Notifier()
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

    if slack_client.rtm_connect():
        print("SubStackBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command is not None and channel is not None:
                notifier.send_slack("I received your command: `{}`".format(command))
                handle_command(command)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")