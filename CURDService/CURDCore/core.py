
import os
from django.conf.urls import url, include
from django.shortcuts import HttpResponse,render
class BaseCurdAdmin():
    '用于根据model生成url及数据的增删改查'
    list_display='__all__'
    def __init__(self,model_class,site):
        self.model_class=model_class
        self.site=site
        self.request=None

    @property
    def urls(self):
        info=self.model_class._meta.app_label,self.model_class._meta.model_name     #model下的表的类（先前被封装了）会被传到此处
        print(info,'info=---------')
        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            url(r'^add/$', self.add_view, name='%s_%s_add' % info),
            url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
            url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % info),
        ]
        return urlpatterns

    def changelist_view(self,request):
        self.request=request
        result_list=self.model_class.objects.all()
        content={
            'list_dispaly':self.list_display,
            'data_list':result_list,
            'base_curd_admin_obj':self
        }
        print(self.list_display,'list_display')
        print(self.model_class.objects.all())
        #self.model_cls.objects.create(username='ender',email='123@123.com')
        #return render(request,'my_curd/changlist_view.html',content)
        #return HttpResponse('it is ok')
        return render(request,'my_curd/changlist_view.html',{'result_list':result_list})

    def add_view(self,request):
        return HttpResponse('add')
    def change_view(self,request):
        pass
    def delete_view(self,request):
        return HttpResponse('delete')




class BaseCurdSite():   #用于注册model
    def __init__(self):
        self._registry={}
        self.namespace='curd'
        self.app_name='curd'

    def register(self,model_class,reg=BaseCurdAdmin):
        self._registry[model_class]=reg(model_class,self)   #self._registry={'User':BaseCurdAdmin(User,BaseCurdSite),....}
        print(self._registry)
    def get_urls(self):
        from django.conf.urls import url,include
        ret=[
            url('login/',self.login,name='login'),
            url('logout/',self.logout,name='logout'),
        ]
        #使用include生成url
        for model_cls,base_curd_admin_obj in self._registry.items():
            app_label=model_cls._meta.app_label
            model_name=model_cls._meta.model_name         #model_cls._meta 是app下的表明
            print(model_cls._meta,model_name,model_name,'-----app_name,app_lable')
            temp=url(r'^%s/%s/'%(app_label,model_name),include(base_curd_admin_obj.urls))
            ret.append(temp)
        return ret

    @property
    def urls(self):
        print(self.get_urls(),self.app_name,self.namespace,'self--')
        return self.get_urls(),self.app_name,self.namespace

    def login(self,request):
        '登录'
        return HttpResponse('login')
    def logout(self,request):
        '登出'
        return HttpResponse('logout')


site=BaseCurdSite()
