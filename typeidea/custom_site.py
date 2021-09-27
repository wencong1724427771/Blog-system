from django.contrib.admin import AdminSite
"""定制site"""


class CustomSite(AdminSite):
    site_header = 'Typeidea'
    site_title = 'Typeidea 管理后台'
    index_title = '首页'


custome_site = CustomSite(name='cus_admin')