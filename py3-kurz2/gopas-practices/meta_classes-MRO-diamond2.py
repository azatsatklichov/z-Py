

print("Diamond issue - http://www.aizac.info/a-solution-to-the-diamond-problem-in-python/")

print("C3 linearization - https://en.wikipedia.org/wiki/C3_linearization")

class Parent(object):
    def __init__(self, name, serial_number):
        self.name = name
        self.serial_number = serial_number


class ChildA(Parent):
    def __init__(self, name, serial_number):
        self.name = name
        self.serial_number = serial_number
        super(ChildA, self).__init__(name = self.name, serial_number = self.serial_number)

    def speak(self):
        print("I am from Child A")


class ChildB(Parent):
    def __init__(self, name, serial_number):
        self.name = name
        self.serial_number = serial_number
        super(ChildB, self).__init__(name = self.name, serial_number = self.serial_number)

    def speak(self):
        print("I am from Child B")


class GrandChild(ChildA, ChildB):
    def __init__(self, a_name, b_name, a_serial_number, b_serial_number):
        self.a_name = a_name
        self.b_name = b_name
        self.a_serial_number = a_serial_number
        self.b_serial_number = b_serial_number
        super(GrandChild, self).__init_( something )