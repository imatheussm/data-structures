def contains_Error(source, destination, container):
    if source not in container.keys():
        print("It seems your source doesn't exist.")
        return True

    if destination not in container.keys():
        print("It seems your destination doesn't exist.")
        return True

    return False

def limitError(start, end, n):
    if start not in range(0, n) or end not in range(0, n):
        print("It seems you did something wrong. Please check the values you gave.")
        return True
    return False