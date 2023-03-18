import importlib
projFile = importlib.import_module("DataProcessing.fab.fabfile")


def fetchUsers():
    rating_matrix, mean_centered_matrix = pp.matrix_creation()
    return rating_matrix

def recommendUser():
    for user in fetchUsers():
        print(user)
