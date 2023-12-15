class parent:
    def __init__(self):
        print("parent's __init__() invoked")
class Derived(parent):
    def __new__(self):
        print("Derived's __new__() invoked")
    def __init__(self):
        print("Derived's __init__() invoked")
def main():
    obj1 = parent()
    obj2 = Derived()
main()