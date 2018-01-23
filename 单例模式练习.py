#单例模式：该类最多只有一个实例
#多类模式
class A:
    def __init__(self):
        pass

a1=A()
a2=A()
print(a1,a2)
#单例模式写法：一是，文件导入的方式，每次都会使用此文件下的一个类，这也是单例模式
#二：下方代码
class B:
    _instance=None
    def __init__(self):
        pass
    @classmethod
    def get_instance(cls):
        if cls._instance:     #如果已经存在实例
            return cls._instance
        else:
            obj=cls()   #创建一个类
            cls._instance=obj
            return obj
b1=B.get_instance()   #按照此方法创建，永远是同一个实例化的对象
b2=B.get_instance()
print(b1,b2)

#单例写法三：使用__new__方法,__new__方法会比__init__方法先执行
#__new__() 方法是在类准备将自身实例化时调用。
class C:
    _instance=None
    def __init__(self):
        pass
    def __new__(cls, *args, **kwargs):
        if cls._instance:
            return cls._instance
        else:
            obj=object.__new__(cls,*args,**kwargs)
            cls._instance=obj
            return obj
c1=C()
c2=C()
print(c1,c2,id(c1),id(c2))