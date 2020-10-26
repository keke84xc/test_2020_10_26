from django.shortcuts import render

from django.http import HttpResponse

from .models import Grades,Students

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.db.models import Max,Min,Sum

from django.db.models import Q

# Create your views here.


def students2(request):
    #querySet_students = Students.objects.all()
    querySet_students = Students.stuObj.all()
    return render(request,'myApp/students.html',{'students':querySet_students})

def students_limit(request):
    #querySet_students = Students.objects.all()
    #返回第一页，每页4条记录
    #querySet_students = Students.stuObj.all()[0:4]
    #返回第二页，每页4条记录
    #1、模糊查询：包含
    #querySet_students = Students.objects.all().filter(sname__contains='测')
    #2、模糊查询：以XXX开头
    querySet_students = Students.objects.all().filter(sname__startswith='测')

    #3、模糊查询：in包含,也可以pk__in=[1,2]
    #querySet_students = Students.objects.all().filter(id__in=[2,4,6])

    #4、模糊查询：年龄大于30
    # querySet_students = Students.objects.all().filter(sage__gt=30)
    # maxAge = Students.objects.all().aggregate(Max('sage'))
    # print(maxAge)

    #5、模糊查询：班级是1或者2的学生列表
    #querySet_students = Students.objects.filter(Q(sgrade_id=1)|Q(sgrade_id=2))
    #班级编号小于3且大于0的学生列表
    #querySet_students = Students.objects.filter(Q(sgrade_id__lt=3) & Q(sgrade_id__gt=0))

    #班级编号小于3且名字不是‘薛艳梅’的学生列表
    #在 Q 对象的前面使用 ~ 来代表“非”
    querySet_students = Students.objects.filter(Q(sgrade_id__lt=3) & ~Q(sname='薛艳梅'))

    #关联查询，查询含有描述为薛艳梅这个学生的班级对象
    grade = Grades.objects.all().filter(students__scontend__contains='薛艳梅')

    print(grade)

    return render(request,'myApp/students.html',{'students':querySet_students})

def students_limit_offset(request,page):

    #第一页:0,5、第二页：5,10，第三页：10,15
    #规律：(page-1)*5,page*5
    current_page = int(page)
    num_pre_page = 4
    querySet_students = Students.objects.all()[(current_page-1)*num_pre_page:current_page*num_pre_page]
    return render(request,'myApp/students.html',{'students':querySet_students})


    #return HttpResponse('接收到的参数为：%s' %(page))

def students_fenye(request,page):

    #querySet_students = Students.stuObj.all()

    querySet_students = Students.objects.all()


    print(querySet_students)
    num_pre_page = 4

    current_page = int(page)

    querySet_students_current = get_paginator_page(num_pre_page,querySet_students,current_page)

    return render(request,'myApp/students.html',{'students':querySet_students_current})

def get_paginator_page(num_prePage,querySet,currentPage):
    #设置每页显示数据
    paginator = Paginator(querySet,num_prePage)
    #print(paginator.num_pages)
    #第一页对象：<QuerySet [<Guest: 嘉宾名称张三>]>
    #print(paginator.object_list)
    #page = request.GET.get('page')
    try:
        contacts = paginator.page(currentPage)
    except PageNotAnInteger:
        #如果page不是整形，传递第一页
        contacts = paginator.page(1)
    except EmptyPage:
        #如果页数超出范围，传递最后一页
        contacts = paginator.page(paginator.num_pages)
    return contacts



def addstudent(request):
    grade = Grades.objects.get(pk=1)
    #方法1：使用模型类的类方法，创建对象，时间使用默认的
    #stu = Students.createStudent('刘德华',34,True,'我叫刘德华',grade)
    #方法2：使用模型管理器类对象的方法创建对象，时间使用默认的
    stu = Students.stuObj.createStudent('蔡依林',33,False,'我叫蔡依林',grade)
    stu.save()
    return HttpResponse('插入成功')

def exception(request):
    try:
        #查询一个id不存在的学生
        #stu = Students.stuObj.get(pk=100)
        #查询结果返回多个对象
        grade = Grades.objects.get(isDelete=False)
    except Exception as e:

        #MultipleObjectsReturned('get() returned more than one Grades -- it returned 3!',)
        print("%r" %e)
        #第8次提交
    return HttpResponse("测试888")
