import inspect
from .exceptions import CtxException
from ctx import ctx as app_ctx
import importlib
from .helpers import snake_to_camel


class Ctx(object):
    ctx = None  # type: app_ctx.Ctx
    _ctx_root = ""

    _mod_name = ""

    def init_ctx_service(self, ctx_root, mod_name):
        # 防止此方法被调用多次
        if self._ctx_root != "":
            raise CtxException('method deny, invoke: {}@{}.{}'.
                               format(inspect.stack()[0][3], self.__module__, self.__class__.__name__))
        self._ctx_root = ctx_root
        self._mod_name = mod_name
        self._init()

    def _init(self):
        pass

    def _load_child(self, cls, *args, **kwargs):
        if not self._ctx_root:
            raise CtxException('can not loadC until construct obj, invoke: {}@{}.{}'.
                               format(inspect.stack()[0][3], self.__module__, self.__class__.__name__))

        child_module_prefix = '{}.service.{}.child.'.format(self._ctx_root, self._mod_name)
        if type(cls) == str:
            module_name = child_module_prefix + cls
            module = importlib.import_module(module_name)
            # get class
            class_name = snake_to_camel(cls)
            try:
                cls = getattr(module, class_name)
            except AttributeError as e:
                raise CtxException("can not load class: {}.{}".format(module_name, class_name))
        else:
            if not cls.__module__.startswith(child_module_prefix):
                raise CtxException("child class must startswith {}, module:'{}' can not load child: {}, ".
                                   format(child_module_prefix, child_module_prefix, cls))

        # get class instance
        service = cls(*args, **kwargs)
        if isinstance(service, Ctx):
            setattr(service, 'ctx', self.ctx)
            service.init_ctx_service(self._ctx_root, self._mod_name)
        return service

    # rpc 配置
    _rpc = {
        'host': '',     # 网关地址
        'method': [],   # 方法名 减少无用的远程调用
    }

    # 排除这些字段，暂时无用，rpc 功能不提供
    _skip_get_attr = []

    # def __getattr__(self, method):
    #     if method in self._skip_get_attr:
    #         return None
    #
    #     if self._rpc['host'] == "" or len(self._rpc['method']) == 0 or (method not in self._rpc['method']):
    #         raise CtxException('undefined method: {}@{}.{}'.format(method, self.__module__, self.__class__.__name__))
    #
    #     def func(*args, **kwargs):
    #         return self._invoke_rpc(method, *args, **kwargs)
    #
    #     return func

    # 执行远程Rpc调用逻辑，方便子类进行更灵活的操作如:显式调用,异步调用等
    def _invoke_rpc(self, method, *args, **kwargs):
        # do rpc, like below:
        # rpc = JsonRpcClient(self.rpc['host'])
        # return rpc.exec(self.mod_name, method, *args, **kwargs)
        pass

