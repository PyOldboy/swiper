import logging

from django.utils.deprecation import MiddlewareMixin

from common import errors
from libs.http import render_json

err_log = logging.getLogger('err')

class AuthMiddleware(MiddlewareMixin):
    white_list = [
        '/',
        '/api/user/vcode/fetch',
        '/api/user/vcode/submit',
        '/qiniu/callback'
    ]

    def process_request(self,request):
        if request.path in self.white_list:
            return

        uid = request.session.get('uid')
        if not uid:
            return render_json(data='用户未登录', code=errors.LoginRequired.code)
        else:
            request.uid = uid

class LogicErrMiddleware(MiddlewareMixin):
    '''逻辑异常处理中间件'''

    def process_exception(self, request, exception):
        if isinstance(exception, errors.LogicErr):
            err_log.error(f'逻辑异常: {exception.code}: {exception.data}')
            return render_json(exception.data, exception.code)