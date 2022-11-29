def announce(f):
    def wrapper():
        print("About to run the funciton")
        f()
        print("Done runnning the funciont")
    return wrapper

@announce
def hello():
    print("hello, world")

hello()