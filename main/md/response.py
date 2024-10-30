"""
统一返回格式
"""
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.handlers.base import BaseHandler


class ResponseMiddleWare(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
