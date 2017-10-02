#!/usr/bin/python 2.7

from slackclient import SlackClient
import os
import time


class Notifier:
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

    def __init__(self):
        self.slackToken = None
        self.slackToken = os.environ.get('SLACK_BOT_TOKEN')
        if self.slackToken == '':
            raise "please put SLACK_BOT_TOKEN to system environment"

    def send_slack(self, message):
        slack_client = SlackClient(self.slackToken)
        while True:
            api_call = slack_client.api_call("users.list")
            if api_call.get('ok'):
                slack_client.api_call(
                    "chat.postMessage",
                    channel="#general",
                    text=message,
                    as_user=True
                )
                break
            else:
                print "Cant load users.list", api_call
                time.sleep(2)

    def erlog(self, message):
        message = "*[Development substack]* " + message
        self.send_slack(message)
