import time
import textwrap as tr
from string import punctuation
from events import *

#number of letters per line
screenWidth = 100
pauses = True

def same2(phrase):
    return [phrase, None, phrase]


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


class Printer:

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

            if pauses == False:
                sleep_time1 = 0
                sleep_time2 = 0

            # wait before printing message
            time.sleep(sleep_time1)
            self.print_width(text)
            # wait after printing message
            time.sleep(sleep_time2)

    def print_width(self, text):
        #prints text within screenWidth
        print(tr.fill(text, width=screenWidth))


    def controls(self):
        self.print("""
    Controls:

    To EXAMINE your surroundings or a specific item, type 'look' before the name of what you want to examine. (eg.'look book', 'look around')
    To USE a specific object, type 'use' before the name of the object you want to use. (eg.'use stick', 'use coin')
    View your INVENTORY by typing 'inventory'.
    Feel free to experiment with your commands by looking for other shortcuts! ;)

    If you ever need to review this message, type 'help'.
    To open setting menu, type 'settings'.
    You can EXIT the game at any moment by typing 'exit'.
    """)

    def onoff(self, boolean):
        if boolean == True:
            return "ON"
        else:
            return "OFF"

    def settings(self):
        from object_use import back
        import audio
        global screenWidth, pauses
        while True:
            settings_list = [
                ["Sound effects", self.onoff(audio.sfx)],
                ["Pauses between text", self.onoff(pauses)],
                ["Number of letters per line", screenWidth],
                             ]
            ans = None
            for i in range(len(settings_list)):
                self.print(str(i+1) + " - " + str(settings_list[i][0]) + ": " + str(settings_list[i][1]))
            ans = multi(None, "Enter number to change setting. Press b to go back. ", (back, "1", "2", "3"),
                        try_again=None, original_result=False, tuples=False)
            if ans == 0:
                return
            elif ans == 1:
                audio.sfx = not audio.sfx
            elif ans == 2:
                pauses = not pauses
            else:
                screenWidth = int(input("Enter " + str(settings_list[int(ans-1)][0]).lower() + " "))


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
        from game_objects import spider
        #If counter above 0 (ticking), take value from list index
        if self.counter > 0:
            tock = self.tickActions[len(self.tickActions) - self.counter]
            #If this value exists...
            if tock:
                #...AND it is a string...
                if isinstance(tock, str):
                    #...AND tock is split into sections, first part is a function

                    if 'SP1' in tock:
                        tock = tock.replace("SP1", spider.nickname[1])
                    if 'SP0' in tock:
                        tock = tock.replace("SP0", spider.nickname[2])

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


