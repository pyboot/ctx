import io
import traceback
from typing import Callable
import functools


def exception_to_str(e: BaseException):
    # return traceback.format_exc()
    return "{module_name}.{class_name}: {message}\nTraceback:\n{tb}".format(
        module_name=e.__class__.__module__,
        class_name=e.__class__.__name__,
        message=get_exception_message(e),
        tb=get_exception_trace(e),
    )


def get_exception_trace(e: BaseException):
    sio = io.StringIO()
    # traceback.print_tb(sys.exc_info()[2], limit=None, file=sio)
    traceback.print_tb(e.__traceback__, limit=None, file=sio)
    s = sio.getvalue()
    sio.close()
    if s[-1:] == "\n":
        s = s[:-1]
    return s


def get_exception_message(e: BaseException):
    """
    获取异常的message

    因为在python中没有要求异常的一定是字符串，所以不同的异常类可能又不同的方式，这里统一做处理，其他地方进行调用
    :param e:
    :return:
    """
    try:
        message = str(e)
    except BaseException as e:
        # isinstance(e, ClickException)
        if hasattr(e, 'message'):
            message = e.message
        else:
            message = 'no ex message? 看到这个消息请联系shine这个方法~get_exception_message'

    return message


def thread_exception_decorator(callback: Callable, *callback_args, **callback_kwargs):
    """
    多线程异常回调处理装饰器
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BaseException as e:
                if isinstance(e, SystemExit):
                    raise e

                if callback:
                    callback(*callback_args, **callback_kwargs, origin={
                        "args": args,
                        "kwargs": kwargs,
                        "e": e
                    })

            # import sys
            # sys.exit(1)

        return wrapper

    return decorator

