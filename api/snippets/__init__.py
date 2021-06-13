import pkgutil

types = {}


class NoSnippetInModuleException(Exception):
    pass


def load_types(path):
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
            print("Skipping module {}: {}".format(name, e))


load_types(__path__)
