import uuid

from django.utils.deprecation import MiddlewareMixin

THE_YEARS = 60*60*24*365


class UserIDMiddleware(MiddlewareMixin):
    """获取用户的Uid"""
    def process_response(self, request, response):
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)    # 把resquest.uid添加到响应头
        # print(request.uid,'xxxxx')
        response.set_cookie('USER_KEY',uid,max_age=THE_YEARS)
        return response

    def generate_uid(self,request):
        try:
            uid = request.COOKIES['USER_KEY']
            # print(uid,'11111')
        except KeyError:
            # print('生成uid')
            uid = uuid.uuid4().hex
        return uid