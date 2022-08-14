import time
import textwrap as tr
from string import punctuation
from events import *


def same2(phrase):
    return [phrase, None, phrase]


class Printer:
    #number of letters per line
    screenWidth = 100

    def print(self, text):
        sleep_time1 = 0
        sleep_time2 = 0
        messages = text.split("\n")
        for message in messages:
            text = message.strip()
            #Take letters from beginning of string same as the number of '~'
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

            # wait before printing message
            time.sleep(sleep_time1)
            self.print_width(text)
            # wait after printing message
            time.sleep(sleep_time2)

    def print_width(self, text):
        #prints text within screenWidth
        print(tr.fill(text, width=self.screenWidth))

    #Maybe print .format(S=SpiderName, s=spiderName) here?


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


"""
    There could be more setting options later on:
    screenWidth, speedrun mode where there isn't a pause between messages, etc.
"""


#Time passage
class Tickable(Printer):
    def __init__(self, tick_actions):
        self.counter = 0
        self.tickActions = tick_actions

    #Set counter to value it is ticking down from
    def start_tick(self):
        self.counter = len(self.tickActions)

    #Return to counter to 0
    def stop_tick(self):
        self.counter = 0

    def tick(self):
        #If counter above 0 (ticking), take value from list index
        if self.counter > 0:
            tock = self.tickActions[len(self.tickActions) - self.counter]
            #If this value exists...
            if tock:
                #...AND it is a string...
                if isinstance(tock, str):
                    #...AND tock is split into sections, first part is a function
                    if '/' in tock:
                        text = tock.split('/')
                        eval(text[0] + f"({text})")
                    #Else, print message
                    else:
                        self.print(tock)
                #Execute function if value is not a string
                else:
                    tock()
            #Diminish counter by 1
            self.counter -= 1


#Multiple-choice questions
def multi(item, prompt, responses, try_again, original_result, tuples):
    ans = input(prompt)
    correct = None
    while True:
        #player response is lower-cased, space-stripped and punctuation-stripped
        new = ans.lower().rstrip().strip(punctuation)
        for response in responses:
            #If responses exist in tuples inside the list
            if tuples:
                # Looks for response inside tuples
                for res in response:
                    if new in res:
                        correct = response
            #Else, looks for response inside list
            else:
                if new in response:
                    correct = response
            #If valid response is found
            if correct:
                #if programs requests, return valid response
                if original_result:
                    return correct
                #else, return response number (the order it was found in, index, whatever)
                else:
                    return responses.index(correct)
        #loops program until valid answer - activates try_again function if it exists
        if try_again:
            try_again(item, ans)
        ans = input(prompt)


#Yes/no questions
def yn(prompt):
    ans = input(prompt)
    while True:
        # player response is lower-cased, space-stripped and punctuation-stripped
        new = ans.lower().rstrip().strip(punctuation)
        #consecutively repeating letters are removed (eg. 'nooooo' becomes 'no')
        new = ''.join(sorted(set(new), key=new.index))
        responses = (['y', 'yes', 'yas', 'yeah', 'yesir', 'yup', 'yep', 'ya', 'ye'],
                     ['n', 'no', 'nah', 'nah bruv', 'nup', 'nop', 'nope'])
        # Looks for response inside list
        for response in responses:
            if new in response:
                return responses.index(response)
        #Loops if valid response is not given
        ans = input(prompt)
