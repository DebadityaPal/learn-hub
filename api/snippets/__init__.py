import pkgutil
from api.colors import print_error

types = {}


class NoSnippetInModuleException(Exception):
    pass


def load_types(path):
    """Loads all the Snippet Sub Modules and stores it in the dictionary."""
    if type(path) != list:
        path = [path]
    for loader, name, _ in pkgutil.walk_packages(path):
        module = loader.find_module(name).load_module(name)
        try:
            if name in dir(module):
                types[name.lower()] = module.__dict__[name]
            else:
                raise NoSnippetInModuleException("No class %s" % name)

        except Exception as e:
            print_error("Skipping module {}: {}".format(name, e))


load_types(__path__)
