import os, sys

# Shamelessly taken from https://stackoverflow.com/a/6246478
# Adds all classes from submodules in the models directory to sys.modules so we
# can do an `import *` from migration_app and allow Flask-Migrate to create
# all of the necessary migrations from our table definitions.

path = os.path.dirname(os.path.abspath(__file__))

for py in [f[:-3] for f in os.listdir(path) if f.endswith(".py") and f != "__init__.py"]:
    mod = __import__(".".join([__name__, py]), fromlist=[py])
    classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
    for cls in classes:
        setattr(sys.modules[__name__], cls.__name__, cls)
