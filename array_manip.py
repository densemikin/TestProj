def gg():
    print("Start")
    index = 0
    while True:
        yield index
        index += 1


a = (i for i in gg())
print(next(a))
print(next(a))
print(next(a))
print(next(a))