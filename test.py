class C:
    def run(self):
        print('машина едет по другому')
        print(self.field_1)


class A(C):
    field_1 = 'Привет'

    def run(self):
        super().run()


instances = {}


def getInstance(aClass, *args):
    if aClass not in instances:
        instances[aClass] = aClass(*args)
    return instances[aClass]


def singleton(aClass):
    def onCall(*args):
        return getInstance(aClass, *args)

    return onCall


@singleton
class Spam:
    def __init__(self,val):
        self.val = val



class Parent(object):
    x = None  # default value
    def __init__(self):
        method = self.run
        print(self.x)
        method()

class someChild(Parent):
    x = 10
    def __init__(self):
        super().__init__()

    def run(self):
        print('едет')

########################

class ParentTest(object):
    def do(self):
        print(self.run())

class otherChild(ParentTest):
    def run(self):
        print('едет')

b = otherChild()
b.do()


#a = someChild()
# output: 10

