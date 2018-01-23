
import os
from django.conf.urls import url, include
from django.shortcuts import HttpResponse,render,redirect
from django.urls import reverse
import copy
class BaseCurdAdmin():
    '用于根据model生成url及数据的增删改查'
    list_display='__all__'
    #list_display = ['username','email']
    add_edit_modelform=None
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
        result_lists=self.model_class.objects.all()
        #---------------分页开始------------------------
        changlist_name= '%s_%s_changelist' % (self.model_class._meta.app_label, self.model_class._meta.model_name)
        changlist_url=reverse('%s:%s'%(self.site.namespace,changlist_name))
        print(changlist_url,'changlist_url--------------')
        from utils import my_pager
        current_page=request.GET.get('page')
        page_params_dict=copy.deepcopy(request.GET)
        page_params_dict._mutable=True
        pagers=my_pager.MyPagination(current_page,result_lists.count(),changlist_url,page_params_dict)
        result_list=result_lists[pagers.start_data:pagers.data_end]
        pager_tags=pagers.pager()
        #--------------分页结束-------------------------
        #添加的url  add_url
        from django.http.request import QueryDict
        parms_dict=QueryDict(mutable=True)
        name='%s_%s_add' % (self.model_class._meta.app_label,self.model_class._meta.model_name)
        add_url_temp=reverse('%s:%s'%(self.site.namespace,name))

        #name_delete='%s_%s_delete' % (self.model_class._meta.app_label,self.model_class._meta.model_name)
        #delete_temp=reverse('%s:%s'%(self.site.namespace,name_delete),args=self.model_class.id)
        if request.method=='GET':
            parms_dict['_changelistfilter']=request.GET.urlencode()
        add_url='{0}?{1}'.format(add_url_temp,parms_dict.urlencode())
        #delete_url='{0}?{1}'.format(delete_temp,parms_dict.urlencode())
        content={
            'list_dispaly':self.list_display,
            'data_list':result_list,
            'base_curd_admin_obj':self,
            'add_url':add_url,
            'pager_tags':pager_tags
        }
        print(self.list_display,'list_display')
        print(self.model_class.objects.all())
        return render(request,'my_curd/changlist_view.html',content)

    def get_add_edit_modelform(self):
        from django.forms import ModelForm
        if self.add_edit_modelform:   #如果用户有自定义的modelform则使用用户自定义的
            return self.add_edit_modelform
        else:
            class DataModelForm(ModelForm):     #创建一个ModelForm用于增加和修改数据
                class Meta:
                    model = self.model_class
                    fields = "__all__"
            return DataModelForm
    def add_view(self,request):  #新增数据
       if request.method=='GET':
           add_modelform_obj=self.get_add_edit_modelform()()
           from django.forms.models import ModelMultipleChoiceField, ModelChoiceField
           for form_obj in add_modelform_obj:
               if isinstance(form_obj.field, ModelChoiceField):  # 说明字段带有ForeignKey或ManytoMany字段
                   print(form_obj.field.queryset, form_obj.field.queryset.model._meta.model_name, form_obj.field.queryset.model._meta.app_label,type(form_obj), 'form_obj-----')
               print(form_obj.name,form_obj.label)
       else:
           add_modelform_obj = self.get_add_edit_modelform()(data=request.POST,files=request.FILES)
           if add_modelform_obj.is_valid():
               add_obj=add_modelform_obj.save()      #保存
               popup_id=request.GET.get('popup_id')
               if popup_id:      #如果存在，说明是通过popup添加的数据
                   data_dict={'pk':add_obj.pk,'text':str(add_obj),'popup_id':popup_id}
                   return render(request,'my_curd/popup_response.html',{'data_dict':data_dict})
               else:    #正常的添加数据
                   print(add_modelform_obj.cleaned_data,'接收到的正确的数据----')
                   name = '%s_%s_changelist' % (self.model_class._meta.app_label, self.model_class._meta.model_name)
                   changelist_url_temp = reverse('%s:%s' % (self.site.namespace, name))
                   changelist_url = '{0}?{1}'.format(changelist_url_temp, request.GET.get('_changelistfilter'))
                   return redirect(changelist_url)  #'重定向到changlist_view页面'
       return render(request,'my_curd/add_data.html',{'form':add_modelform_obj})

    def change_view(self,request,pk):#编辑数据
        obj=self.model_class.objects.filter(id=pk).first()
        if request.method=='GET':#返回带有数据的modelform
            edit_model_form_obj=self.get_add_edit_modelform()(instance=obj)
        else:
            edit_model_form_obj=self.get_add_edit_modelform()(instance=obj,data=request.POST,files=request.FILES)
            if edit_model_form_obj.is_valid():
                edit_model_form_obj.save()
                name = '%s_%s_changelist' % (self.model_class._meta.app_label, self.model_class._meta.model_name)
                changelist_url_temp = reverse('%s:%s' % (self.site.namespace, name))
                changelist_url = '{0}?{1}'.format(changelist_url_temp, request.GET.get('_changelistfilter'))
                return redirect(changelist_url)  # '重定向到changlist_view页面'
        return render(request,'my_curd/edit_data.html',{'form':edit_model_form_obj})
        # info = self.model_class._meta.app_label, self.model_class._meta.model_name
        # return HttpResponse('%s-%s编辑change'%info)
    def delete_view(self,request,pk):
        '删除某条数据'
        print(pk,'------------pk值---------')
        if pk:
            self.model_class.objects.filter(id=pk).delete()
            name = '%s_%s_changelist' % (self.model_class._meta.app_label, self.model_class._meta.model_name)
            changelist_url_temp = reverse('%s:%s' % (self.site.namespace, name))
            changelist_url = '{0}?{1}'.format(changelist_url_temp, request.GET.get('_changelistfilter'))
            return redirect(changelist_url)  # '重定向到changlist_view页面'
        else:
            return HttpResponse('没有找到id值')


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
