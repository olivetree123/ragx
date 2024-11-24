from threading import local

from django.utils.deprecation import MiddlewareMixin

# 参考1：https://github.com/jedie/django-tools/blob/main/django_tools/middlewares/ThreadLocal.py
# 参考2：https://github.com/Alir3z4/django-crequest/blob/master/crequest/middleware.py
# 参考3：https://hustyichi.github.io/2018/08/22/LocalProxy-in-flask/

_thread_locals = local()

# def current_user(null=False):
#     request = get_request()
#     if null:
#         return getattr(request, "user_uid", None)
#     return getattr(request, "user_uid")


def current_project():
    request = getattr(_thread_locals, "request")
    return getattr(request, "project_id")


class CurrentRequestMiddleware(MiddlewareMixin):
    """保存当前请求的一些全局变量"""

    def process_request(self, request):
        # 在视图处理请求之前调用
        _thread_locals.request = request

    def process_response(self, request, response):
        # 在视图处理请求之后调用
        return response

    def process_exception(self, request, exception):
        # 在视图抛出异常时调用
        return None
