__author__ = 'cWX205128'

# some mine little idea...


def do_sth(para):
    print 'do sth.', para


def return_class():
    class Class1():
        def __init__(self):
            self.name = 'class1'

        def pit(self):
            print 'xxxx', self.name
            return 'pit'

    return Class1


def closure():
    x = 123

    def a():
        print x
    return a


do_sth('xxx')
print return_class()().pit()
