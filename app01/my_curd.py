
from app01 import models
from CURDService.CURDCore import core_func
from django.utils.safestring import mark_safe
from django.urls import reverse


# def edit(model_obj, base_curd_admin_obj):
#     print(model_obj.id, 'edit-----')   #id
#     print(base_curd_admin_obj.model_class._meta.app_label,base_curd_admin_obj.model_class._meta.model_name)
#     #app 名称及表名
#     edit_tag='<a href="/curd/%s/%s/%s/change/">编辑</a>'%(base_curd_admin_obj.model_class._meta.app_label,
#                                                 base_curd_admin_obj.model_class._meta.model_name,
#                                                 model_obj.id)
#     return mark_safe(edit_tag)
class UserCurdAdmin(core_func.BaseCurdAdmin):
    def edit(self, model_obj=None,is_header=False):
        if is_header:
            return '编辑'
        else:
            from django.http.request import QueryDict
            parms_dict = QueryDict(mutable=True)
            if self.request.method == 'GET':
                parms_dict['_changelistfilter'] = self.request.GET.urlencode()
            name = '{0}:{1}_{2}_change'.format(self.site.namespace, model_obj._meta.app_label,
                                               model_obj._meta.model_name)
            url = reverse(name, args=(model_obj.pk,))  # s生成的结果同上方的edit   pk和id同样
            edit_url = '{0}?{1}'.format(url, parms_dict.urlencode())
            print(model_obj.id, 'edit-----')  # id
            edit_tag='<a href="%s">编辑</a>' %edit_url
            #edit_tag = '<a href="/curd/%s/%s/%s/change/">编辑</a>' % (model_obj._meta.app_label,
                                                                    # model_obj._meta.model_name,
                                                                    # model_obj.id)
            return mark_safe(edit_tag)
    def delete(self,model_obj=None,is_header=False):
        if is_header:
            return '删除'
        else:
            from django.http.request import QueryDict
            parms_dict = QueryDict(mutable=True)
            if self.request.method == 'GET':
                parms_dict['_changelistfilter'] = self.request.GET.urlencode()
            name = '{0}:{1}_{2}_delete'.format(self.site.namespace, model_obj._meta.app_label,
                                               model_obj._meta.model_name)
            url = reverse(name, args=(model_obj.pk,))  # s生成的结果同上方的edit   pk和id同样
            delete_url = '{0}?{1}'.format(url, parms_dict.urlencode())
            print(model_obj.id, 'edit-----')  # id
            delete_tag = '<a href="%s">删除</a>' % delete_url


            # name = '{0}:{1}_{2}_delete'.format(self.site.namespace, model_obj._meta.app_label,
            #                                    model_obj._meta.model_name)
            # url = reverse(name, args=(model_obj.pk,))  # s生成的结果同上方的edit   pk和id同样
            # delete_tag='<a href="%s">删除</a>' %url
            # delete_tag='<a href="/curd/%s/%s/%s/delete/">删除</a>' % (model_obj._meta.app_label,
            #                                                         model_obj._meta.model_name,
            #                                                         model_obj.id)
            return mark_safe(delete_tag)
    def reverse_produce_url(self,model_obj=None,is_header=False):
        '练习反向生成url'
        if is_header:
            return '反向生成url练习'
        else:
            #取namespace的方式
            from CURDService.CURDCore import core_func
            print(self.site.namespace, core_func.site.namespace, 'namespace------------>>>')
            #取model_name的方式
            print(type(model_obj), '---type?', model_obj.__dict__, type(model_obj)._meta.model_name,self.model_class._meta.model_name)
            #取app_label的方式
            print(type(model_obj), '---type?', model_obj.__dict__, type(model_obj)._meta.app_label,self.model_class._meta.app_label)
            #获取namespace及app_name,model_name的方式1,使用type获取model_obj类，然后回去该类的属性
            print(type(model_obj),'---type?',model_obj.__dict__,type(model_obj)._meta.model_name,type(model_obj)._meta.app_label)
            # 获取namespace及app_name,model_name的方式2,使用self 的site属性，site里面封装了BaseCurdSite类，可以直接获取该类的属性
            info=model_obj._meta.app_label,model_obj._meta.model_name
            name = '{0}:{1}_{2}_change'.format(self.site.namespace,model_obj._meta.app_label,model_obj._meta.model_name)
            url=reverse(name,args=(model_obj.pk,))   #s生成的结果同上方的edit   pk和id同样
            print(url,'url=----------')
            return url
    def combine_username_email(self,model_obj=None,is_header=False):
        if is_header:
            return '定制列'
        else:
            print('定制列--------',model_obj.email)
            v='%s--%s'%(model_obj.username,model_obj.email)
            return v

    list_display = ['id','username','email','role','usergroup',edit,delete,reverse_produce_url,combine_username_email]


core_func.site.register(models.User, UserCurdAdmin)
core_func.site.register(models.Role)
core_func.site.register(models.UserGroup)