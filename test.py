class Test():
    def __init__(self, description, dynamicFunction):
        self.counter = 0
        self.description = description
        self.getDescription = dynamicFunction

    def printMe(self):
        print(self.description.format(value=self))
        self.counter += 1

    @property
    def dynamicDescription(self):
        return self.getDescription()


def makeDescription():
    return f"Description {random.randrange(1, 10)}"


test = Test(
    "Hi, I am counter {value.counter}, here is my dynamic description: {value.dynamicDescription}",
    makeDescription
)