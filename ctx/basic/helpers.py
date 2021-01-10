from threading import RLock


def snake_to_camel(word):
    first, *others = word.split('_')
    return first.title() + ''.join(x.title() for x in others)


_missing = object()


class locked_cached_property(object):
    """A decorator that converts a function into a lazy property.  The
    function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value.  Works like the one in Werkzeug but has a lock for
    thread safety.
    """

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func
        self.lock = RLock()

    def __get__(self, obj, typ=None):
        if obj is None:
            return self
        with self.lock:
            value = obj.__dict__.get(self.__name__, _missing)
            if value is _missing:
                value = self.func(obj)
                obj.__dict__[self.__name__] = value
            return value


# 只加载模块文件，但是不加载类
def auto_load_module(dirname, module_prefix):
    import glob
    import importlib
    import os
    modules = glob.glob(os.path.join(dirname, "*.py"))
    print([os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")])
    modules = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]
    for cls in modules:
        module_name = '{}.{}'.format(module_prefix, cls)
        importlib.import_module(module_name)
