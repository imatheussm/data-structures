def contains_Error(source, destination, container):
    if source not in container.keys():
        print("It seems your source doesn't exist.")
        return True

    if destination not in container.keys():
        print("It seems your destination doesn't exist.")
        return True

    return False