from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    white_list = [
        '/api/user/vcode/fetch',
        '/api/user/vcode/submit',
        '/qiniu/callback'
    ]

    def process_request(self,request):
        if request.path in self.white_list:
            return

        uid = request.session.get('uid')
        if not uid:
            return JsonResponse({'code': 1002, 'data': '用户未登录'})