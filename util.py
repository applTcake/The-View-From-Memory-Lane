import time
import textwrap as tr
from string import punctuation
from events import *


class Printer:
    screenWidth = 80

    def print(self, text):
        sleep_time1 = 0
        sleep_time2 = 0
        messages = text.split("\n")
        for message in messages:
            text = message.strip()
            if text.startswith("~~~"):
                sleep_time1 = float(text[3:6])
                text = text[6:]
            elif text.startswith("~~"):
                sleep_time1 = int(text[2:4])
                text = text[4:]
            elif text.startswith("~"):
                sleep_time1 = int(text[1])
                text = text[2:]
            if text.endswith("&&&"):
                sleep_time2 = float(text[-6:-3])
                text = text[:-6]
            elif text.endswith("&&"):
                sleep_time2 = int(text[-4:-2])
                text = text[:-4]
            elif text.endswith("&"):
                sleep_time2 = float(text[-2])
                text = text[:-2]
            time.sleep(sleep_time1)
            self.print_width(text)
            time.sleep(sleep_time2)

    def print_width(self, text):
        print(tr.fill(text, width=self.screenWidth))

    def controls(self):
        self.print("""
    Controls:

    To EXAMINE your surroundings or a specific item, type 'look' before the name of what you want to examine. (eg.'look book', 'look around')
    To USE a specific object, type 'use' before the name of the object you want to use. (eg.'use stick', 'use coin')
    View your INVENTORY by typing 'inventory'.
    Feel free to experiment with your commands by looking for other shortcuts! ;)

    If you ever need to review this message, type 'help'.
    You can EXIT the game at any moment by typing 'exit'.
    """)


class Tickable(Printer):
    def __init__(self, tick_actions):
        self.counter = 0
        self.tickActions = tick_actions

    def start_tick(self):
        self.counter = len(self.tickActions)

    def stop_tick(self):
        self.counter = 0

    def tick(self):
        if self.counter > 0:
            tock = self.tickActions[len(self.tickActions) - self.counter]
            if tock:
                if isinstance(tock, str):
                    if '/' in tock:
                        text = tock.split('/')
                        eval(text[0] + f"({text})")
                    else:
                        self.print(tock)
                else:
                    tock()
            self.counter -= 1


def multi(item, prompt, responses, try_again, original_result, tuples):
    ans = input(prompt)
    correct = None
    while True:
        new = ans.lower().rstrip().strip(punctuation)
        for response in responses:
            if tuples:
                for res in response:
                    if new in res:
                        correct = response
            else:
                if new in response:
                    correct = response
            if correct:
                if original_result:
                    return correct
                else:
                    return responses.index(correct)
        if try_again:
            try_again(item, ans)
        ans = input(prompt)


def yn(prompt):
    ans = input(prompt)
    while True:
        new = ans.lower().rstrip().strip(punctuation)
        new = ''.join(sorted(set(new), key=new.index))
        responses = (['y', 'yes', 'yas', 'yeah', 'yesir', 'yup', 'yep', 'ya', 'ye'],
                     ['n', 'no', 'nah', 'nah bruv', 'nup', 'nope'])
        for response in responses:
            if new in response:
                return responses.index(response)
        ans = input(prompt)
