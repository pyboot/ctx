import importlib
import os
from .basic.exceptions import CtxException
from .service.utils.ctx import Ctx as Utils


class Ctx(object):
    # !!! 此处定义属性只是为了方便 ide 跳转，不要赋值任何初值
    utils: Utils

    ctx_root = "ctx"

    def __getitem__(self, method):
        return getattr(self, method)

    def __getattr__(self, mod_name):
        # import module
        module_name = '{}.service.{}.ctx'.format(self.ctx_root, mod_name)
        module = importlib.import_module(module_name)

        # get class
        class_name = "Ctx"
        try:
            service_class = getattr(module, class_name)
        except AttributeError as e:
            raise CtxException("can not load class: {}.{}".format(module_name, class_name))

        # get class instance
        service = service_class()
        setattr(self, mod_name, service)
        setattr(service, 'ctx', self)
        service.init_ctx_service(self.ctx_root, mod_name)
        return service

    # 多进程用到
    def __getstate__(self):
        return self.__dict__.copy()

    # 多进程用到
    def __setstate__(self, state):
        self.__dict__.update(state)


# _current_pid = 0
# _ctx_obj: Ctx
#
#
# # 进程间单例
# def get_ctx():
#     global _current_pid, _ctx_obj
#     pid = os.getpid()
#     if pid != _current_pid:
#         _ctx_obj = Ctx()
#         # _ctx_obj.utils.init_app()
#         _current_pid = pid
#
#     return _ctx_obj


# 单例
ctx = Ctx()
# ctx.utils.init_app()
