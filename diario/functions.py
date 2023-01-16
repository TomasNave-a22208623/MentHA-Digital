def multiple_appends(listname, *element):
    listname.extend(element)

def most_frequent(List):
    return max(set(List), key = List.count)