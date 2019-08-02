
class Person:

    def __init__(self, firstName, lastName, age):
        self.firstName  = firstName
        self.lastName = lastName
        self.age = age

    def combineName(self):
        return "{} {}".format(self.firstName, self.lastName)

class BackwardsPerson(Person):

    def __init__(self, firstName, lastName, age, style):
        super().__init__(firstName, lastName, age)
        self.style = style

    def combineName(self):
        return "{}, {}".format(self.lastName, self.firstName)

class TestFunction:

    def testFunction1(self):
        print("Tested")
        return False