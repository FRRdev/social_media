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
    def __init__(self, val):
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


def ruble_func(summ):
    if ',' in summ:
        suum1, summ2 = summ.split(',')
        part_1 = rubble_part(suum1)
        part_2 = copy_part(summ2)
        res = part_1 + part_2
        return part_1 + part_2
    else:
        return rubble_part(summ)


def rubble_part(summ):
    our_str_1 = int(summ[-1])
    result = ''

    if len(summ) < 2:
        if int(summ) == 1:
            result = summ + 'рубль'
        elif 5 > int(summ) > 1:
            result = summ + 'рубля'
        elif 4 < int(summ) < 10:
            result = summ + 'рублей'
    else:
        our_str_2 = int(summ[-2])
        if our_str_2 == 1:
            result = summ + 'рублей'
        elif our_str_2 != 1 and our_str_1 == 1:
            result = summ + 'рубль'
        elif our_str_2 != 1 and 5 > our_str_1 > 1:
            result = summ + 'рубля'
        elif our_str_2 != 1 and 4 < our_str_1 < 10:
            result = summ + 'рублей'
        else:
            result = summ + 'рублей'

    return result


def copy_part(summ):
    our_str_1 = int(summ[-1])
    result = ''

    if len(summ) < 2:
        if int(summ) == 1:
            result = summ + 'копейка'
        elif 5 > int(summ) > 1:
            result = summ + 'копейки'
        elif 4 < int(summ) < 10:
            result = summ + 'копеек'
    else:
        our_str_2 = int(summ[-2])
        if our_str_2 == 1:
            result = summ + 'копеек'
        elif our_str_2 != 1 and our_str_1 == 1:
            result = summ + 'копейка'
        elif our_str_2 != 1 and 5 > our_str_1 > 1:
            result = summ + 'копейки'
        elif our_str_2 != 1 and 4 < our_str_1 < 10:
            result = summ + 'копеек'
        else:
            result = summ + 'копеек'

    return result


