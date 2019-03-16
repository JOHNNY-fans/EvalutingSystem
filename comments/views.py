from django.shortcuts import render, redirect
# -*- coding:utf-8 -*-
# Create your views here.
from django.db.models import Count
from django.contrib import auth
from django.db.models import Q
from numpy import *
import datetime
import math
from django.shortcuts import render
from .models import *


def comment_list(request):
    # list_user = Test.objects.all()  # models里的所有数据
    kind = request.GET['kind']  # 得到用户的种类
    username = request.user.username
    if kind == 'students':
        list_comments = Comments.objects.filter(lesson_teacher_id=request.GET['id']).order_by('-num_score')
        #  通过num_score进行倒序排序
        obj_teacher_lesson = LessonTeacher.objects.get(id=request.GET['id'])
        xid = request.GET['id']
        num_comment = Comments.objects.filter(lesson_teacher_id=request.GET['id']).count()
        num_recommend = Comments.objects.filter(lesson_teacher_id=request.GET['id'], recommend=1).count()
        # 计数数据库里有多少个评论
        good = 0
        bad = 0
        for c in list_comments:
            c.publish_time = c.publish_time.strftime('%Y{y}%m{m}%d{d}').format(y=u'年', m=u'月', d=u'日')
            print(c)
            good += (c.num_valuable + c.num_happy)
            bad += c.num_bad
        hot = (num_recommend + good) / (num_comment + good + bad) * 10
        # 计数数据库里recommend=1的，也就是好评的数量
        return render(request, 'user.html',
                      {'comments': list_comments,
                       'teacher_lesson': obj_teacher_lesson,
                       'id': xid,
                       'hot': "{0:.1f}".format(hot),
                       'kind': kind,
                       'log_in': True,
                       'username': username,
                       })  # 把数据交给render函数，函数交给user.html，用数据渲染html
    else:
        obj_teacher_lesson = LessonTeacher.objects.get(id=request.GET['id'])  # 得到这门课程的信息
        xid = request.GET['id']
        return render(request, 'teacher_user.html',
                      {'teacher_lesson': obj_teacher_lesson,
                       'id': xid,
                       'kind': kind,
                       'log_in': True,
                       'username': username,
                       })  # 把数据交给render函数，函数交给teacher_user.html，用数据渲染html


def lesson_all(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            username = request.user.username
            user_info = User.objects.get(username=username)
            data = LessonTeacher.objects.values('id', 'lesson_name', 'teacher_name', 'school', 'introduction', )
            tea_s = LessonTeacher.objects.values('teacher_name', 'school').annotate(Count('teacher_name')).order_by()
            teacher = LessonTeacher.objects.values('teacher_name').annotate(Count('teacher_name')).order_by()
            lesson = list(set(LessonTeacher.objects.values_list('lesson_name', flat=True)))
            tea_les = list(set(LessonTeacher.objects.values_list('teacher_name', 'lesson_name')))
            return render(request, 'index_lesson_all.html',
                          {'lessons': data,
                           'username': username,
                           'teacher_set': teacher,
                           'lesson_set': lesson,
                           'kind': user_info.kind,
                           'log_in': True,
                           'tdata': tea_s,
                           'ldata': tea_les,
                           },
                          )  # 将这里的data作为lessons传给对应的网站
        else:
            return redirect('/login/',
                            {'log_in': False})
    elif request.method == 'POST':
        if request.user.is_authenticated:
            search = request.POST['search_result']
            search_l = LessonTeacher.objects.filter(Q(lesson_name=search))
            search_t = LessonTeacher.objects.filter(Q(teacher_name=search))
            what = 0
            if search_l:
                what = 1
            elif search_t:
                what = 2
            username = request.user.username
            user_info = User.objects.get(username=username)
            data = LessonTeacher.objects.values('id', 'lesson_name', 'teacher_name', 'school', 'introduction', )
            tea_s = LessonTeacher.objects.values('teacher_name', 'school').annotate(Count('teacher_name')).order_by()
            teacher = LessonTeacher.objects.values('teacher_name').annotate(Count('teacher_name')).order_by()
            lesson = list(set(LessonTeacher.objects.values_list('lesson_name', flat=True)))
            tea_les = list(set(LessonTeacher.objects.values_list('teacher_name', 'lesson_name')))
            return render(request, 'index_lesson_all.html',
                          {'lessons': data,
                           'username': username,
                           'teacher_set': teacher,
                           'lesson_set': lesson,
                           'kind': user_info.kind,
                           'log_in': True,
                           'tdata': tea_s,
                           'ldata': tea_les,
                           'search_l': search_l,
                           'search_t': search_t,
                           'searched': search,
                           'what': what
                           },
                          )  # 将这里的data作为lessons传给对应的网站



def comment(request):
    # 这个函数的作用是让你在操作网页上三个按钮时，可以改变数据库里对应的分数，并且在最后可能改变评论的排序
    comment = Comments.objects.get(id=request.GET["cid"])  # 表示对这一条comment做评论操作
    kind = request.GET['kind']
    if request.GET['action'] == "valuable":
        comment.num_valuable += 1
    elif request.GET['action'] == "happy":
        comment.num_happy += 1
    elif request.GET['action'] == "bad":
        comment.num_bad += 1
    else:
        assert False  # 如果走到这里，那就报错
    comment.num_score = comment.num_valuable * 2 + comment.num_happy - comment.num_bad
    comment.save()  # 保存到数据库
    username = request.user.username
    list_comments = Comments.objects.filter(lesson_teacher_id=request.GET['id']).order_by('-num_score')
    #  通过num_score进行倒序排序
    obj_teacher_lesson = LessonTeacher.objects.get(id=request.GET['id'])
    xid = request.GET['id']
    num_comment = Comments.objects.filter(lesson_teacher_id=request.GET['id']).count()
    num_recommend = Comments.objects.filter(lesson_teacher_id=request.GET['id'], recommend=1).count()
    # 计数数据库里有多少个评论
    good = 0
    bad = 0
    for c in list_comments:
        c.publish_time = c.publish_time.strftime('%Y{y}%m{m}%d{d}').format(y=u'年', m=u'月', d=u'日')
        print(c)
        good += (c.num_valuable + c.num_happy)
        bad += c.num_bad
    hot = (num_recommend + good) / (num_comment + good + bad) * 10
    return render(request, 'user.html',
                  {'comments': list_comments,
                   'teacher_lesson': obj_teacher_lesson,
                   'id': xid,
                   'hot': "{0:.1f}".format(hot),
                   'kind': kind,
                   'log_in': True,
                   'username': username,
                   })  # 把数据交给render函数，函数交给user.html，用数据渲染html


# 实现账号的登录功能
def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/lesson_all/')
        else:
            return render(request, 'login.html', {'log_in': False})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            # 用于以后在调用每个视图函数前，auth中间件会根据每次访问视图前请求所带的SEESION里面的ID，去数据库找用户对像，并将对象保存在request.user属性中
            return redirect('/lesson_all/')
        else:
            return render(request, 'login.html',
                          {'log_in': True})


def logout(request):
    auth.logout(request)
    return redirect("/login/",
                    {
                        'log_in': False,
                        'username': request.user.username
                    }
                    )


def teacher_by_lesson(request):
    list_teacher = LessonTeacher.objects.filter(lesson_name=request.GET['lesson'])
    teacher = LessonTeacher.objects.get(id=request.GET['id'])
    kind = request.GET['kind']
    list_comments = Comments.objects.filter(
        Q(lesson_name=request.GET['lesson']) & Q(lesson_teacher_id=request.GET['id']))
    num_best = 0
    num_good = 0
    num_bad = 0
    for i in list_comments:
        if teacher.id == i.lesson_teacher_id:
            if i.recommend == 1:
                num_best = num_best + 1
                num_best += int(i.num_valuable)
                num_good += int(i.num_happy)
                num_bad += int(i.num_bad)
            else:
                num_bad = num_bad + 1
                num_bad += int(i.num_valuable)
                num_good += 0
                num_best += int(i.num_bad)
    teacher.num_best = num_best
    teacher.num_good = num_good
    teacher.num_bad = num_bad
    teacher.save()
    return render(request, 'index_teacher_by_lesson.html',
                  {'teachers': list_teacher,
                   'lesson_name': request.GET['lesson'],
                   'kind': kind})


def lesson_by_teacher(request):
    list_lesson = LessonTeacher.objects.filter(teacher_name=request.GET['teacher'])
    kind = request.GET['kind']
    # 从数据库里按照红色字体过滤内容
    return render(request, 'index_lesson_by_teacher.html',
                  {'lessons': list_lesson,
                   'teacher_name': request.GET['teacher'],
                   'kind': kind})


def back_to_index(request):
    data = LessonTeacher.objects.values('id', 'lesson_name', 'teacher_name')
    kind = request.GET['kind']
    return render(request, 'index_lesson_all.html',
                  {'lessons': data,
                   'kind': kind})


def KNN_teacher(request):
    list_comments = Comments.objects.filter(teacher_name=request.GET['teacher'])
    kind = request.GET['kind']
    num_best = 0
    num_good = 0
    num_bad = 0
    for i in list_comments:
        if i.recommend == 1:
            num_best = num_best + 1
            num_best += int(i.num_valuable)
            num_good += int(i.num_happy)
            num_bad += int(i.num_bad)
        else:
            num_bad = num_bad + 1
            num_bad += int(i.num_valuable)
            num_good += 0
            num_best += int(i.num_bad)

    teacher_data = {"老师1": [45, 2, 9, "优秀"],
                    "老师2": [21, 17, 5, "优秀"],
                    "老师3": [54, 9, 11, "优秀"],
                    "老师4": [39, 0, 21, "优秀"],
                    "老师5": [5, 2, 57, "差评"],
                    "老师6": [3, 2, 65, "差评"],
                    "老师7": [2, 3, 55, "差评"],
                    "老师8": [6, 4, 21, "差评"],
                    "老师9": [7, 46, 4, "一般"],
                    "老师a": [9, 39, 8, "一般"],
                    "老师b": [9, 38, 2, "一般"],
                    "老师c": [8, 34, 17, "一般"],
                    "老师d": [46, 0, 6, "优秀"],
                    "老师e": [34, 4, 10, "优秀"],
                    "老师f": [20, 10, 12, "一般"],
                    "老师g": [23, 17, 18, "一般"],
                    "老师h": [10, 6, 38, "差评"],
                    "老师i": [8, 5, 20, "差评"],
                    "老师j": [6, 30, 13, "一般"],
                    "老师k": [156, 12, 28, "优秀"],
                    "老师l": [128, 32, 32, "优秀"],
                    "老师m": [68, 40, 48, "一般"],
                    "老师n": [70, 49, 56, "一般"],
                    "老师o": [40, 24, 114, "差评"],
                    "老师p": [32, 20, 80, "差评"]
                    }

    x = [num_best, num_bad, num_good]

    KNN = []

    for key, v in teacher_data.items():
        d = math.sqrt((x[0] - v[0]) ** 2 + (x[1] - v[1]) ** 2 + (x[2] - v[2]) ** 2)

        KNN.append([key, round(d, 2)])

    KNN.sort(key=lambda dis: dis[1])

    KNN = KNN[:5]

    labels = {"优秀": 0, "差评": 0, "一般": 0}

    for s in KNN:
        label = teacher_data[s[0]]

        labels[label[3]] += 1

    labels = sorted(labels.items(), key=lambda l: l[1], reverse=True)
    return render(request, 'teacherknn.html',
                  {'teacher': request.GET['teacher'],
                   'good': num_good + num_best,
                   'bad': num_bad,
                   'comment': labels[0][0],
                   'kind': kind})


def teacher_submit(request):  # 这个函数的用处是提交网页上的评测内容并且添加到本地的数据库里
    choice_comment = ChoiceComments()
    kind = request.POST['kind']
    username = request.user.username
    choice_comment.lesson_teacher_id = request.POST['lesson_teacher_id']
    obj_teacher_lesson = LessonTeacher.objects.get(id=request.POST['lesson_teacher_id'])  # 得到这门课程的信息
    if (request.POST["comment"] is not None) and (request.POST["comment"] != '请输入评测内容'):
        choice_comment.comment = request.POST["comment"]
        if request.POST["attitude"] == "5":
            choice_comment.attitude = 5
        elif request.POST["attitude"] == "4":
            choice_comment.attitude = 4
        elif request.POST["attitude"] == "3":
            choice_comment.attitude = 3
        elif request.POST["attitude"] == "2":
            choice_comment.attitude = 2
        elif request.POST["attitude"] == "1":
            choice_comment.attitude = 1

        if request.POST["content"] == "5":
            choice_comment.content = 5
        elif request.POST["content"] == "4":
            choice_comment.content = 4
        elif request.POST["content"] == "3":
            choice_comment.content = 3
        elif request.POST["content"] == "2":
            choice_comment.content = 2
        elif request.POST["content"] == "1":
            choice_comment.content = 1

        if request.POST["method"] == "5":
            choice_comment.method = 5
        elif request.POST["method"] == "4":
            choice_comment.method = 4
        elif request.POST["method"] == "3":
            choice_comment.method = 3
        elif request.POST["method"] == "2":
            choice_comment.method = 2
        elif request.POST["method"] == "1":
            choice_comment.method = 1

        if request.POST["achievement"] == "5":
            choice_comment.achievement = 5
        elif request.POST["achievement"] == "4":
            choice_comment.achievement = 4
        elif request.POST["achievement"] == "3":
            choice_comment.achievement = 3
        elif request.POST["achievement"] == "2":
            choice_comment.achievement = 2
        elif request.POST["achievement"] == "1":
            choice_comment.achievement = 1

        if request.POST["effect"] == "5":
            choice_comment.effect = 5
        elif request.POST["effect"] == "4":
            choice_comment.effect = 4
        elif request.POST["effect"] == "3":
            choice_comment.effect = 3
        elif request.POST["effect"] == "2":
            choice_comment.effect = 2
        elif request.POST["effect"] == "1":
            choice_comment.effect = 1

        choice_comment.save()
        return render(request, 'teacher_user.html',
                      {
                          'teacher_lesson': obj_teacher_lesson,
                          'username': username,
                          'kind': kind,
                          'id': request.POST['lesson_teacher_id'],
                          'log_in': True,
                          'sub': True
                      })
    else:
        return render(request, 'teacher_user.html',
                      {
                          'teacher_lesson': obj_teacher_lesson,
                          'username': username,
                          'kind': kind,
                          'id': request.POST['lesson_teacher_id'],
                          'log_in': True,
                          'sub': False
                      })


def submit(request):  # 这个函数的用处是提交网页上的评测内容并且添加到本地的数据库里
    comment = Comments()
    kind = request.POST.get('kind')
    comment.lesson_teacher_id = request.POST.get('id')
    comment.lesson_name = request.POST.get('lesson_name')
    comment.publish_time = datetime.datetime.now()
    comment.teacher_name = request.POST.get('teacher_name')
    print(comment.teacher_name)
    if request.POST.get("comment") is not None:
        comment.content = request.POST.get("comment")
        comment.recommend = request.POST.get("recommend") == u'推荐'
        comment.num_bad = 0
        comment.num_valuable = 0
        comment.num_happy = 0
        comment.num_score = 0
        comment.save()
        if kind == 'students':
            username = request.user.username
            list_comments = Comments.objects.filter(lesson_teacher_id=request.POST['id']).order_by('-num_score')
            #  通过num_score进行倒序排序
            obj_teacher_lesson = LessonTeacher.objects.get(id=request.POST['id'])
            xid = request.POST['id']
            num_comment = Comments.objects.filter(lesson_teacher_id=request.POST['id']).count()  # 计数数据库里有多少个评测
            num_recommend = Comments.objects.filter(lesson_teacher_id=request.POST['id'], recommend=1).count()
            # 计数数据库里有多少个评论
            good = 0
            bad = 0
            for c in list_comments:
                c.publish_time = c.publish_time.strftime('%Y{y}%m{m}%d{d}').format(y=u'年', m=u'月', d=u'日')
                print(c)
                good += (c.num_valuable + c.num_happy)
                bad += c.num_bad
            hot = (num_recommend + good) / (num_comment + good + bad) * 10
            return render(request, 'user.html',
                          {'comments': list_comments,
                           'teacher_lesson': obj_teacher_lesson,
                           'id': xid,
                           'hot': "{0:.1f}".format(hot),
                           'kind': kind,
                           'log_in': True,
                           'username': username,
                           }
                          )
        else:
            username = request.user.username
            obj_teacher_lesson = LessonTeacher.objects.get(id=request.POST['id'])  # 得到这门课程的信息
            xid = request.GET['id']
            return render(request, 'teacher_user.html',
                          {'teacher_lesson': obj_teacher_lesson,
                           'id': xid,
                           'kind': kind,
                           'log_in': True,
                           'username': username,
                           })
    else:
        if kind == 'students':
            username = request.user.username
            list_comments = Comments.objects.filter(lesson_teacher_id=request.POST['id']).order_by('-num_score')
            #  通过num_score进行倒序排序
            obj_teacher_lesson = LessonTeacher.objects.get(id=request.POST['id'])
            xid = request.POST['id']
            num_comment = Comments.objects.filter(lesson_teacher_id=request.POST['id']).count()  # 计数数据库里有多少个评测         
            num_recommend = Comments.objects.filter(lesson_teacher_id=request.POST['id'], recommend=1).count()
            # 计数数据库里有多少个评论
            good = 0
            bad = 0
            for c in list_comments:
                c.publish_time = c.publish_time.strftime('%Y{y}%m{m}%d{d}').format(y=u'年', m=u'月', d=u'日')
                print(c)
                good += (c.num_valuable + c.num_happy)
                bad += c.num_bad
            hot = (num_recommend + good) / (num_comment + good + bad) * 10
            return render(request, 'user.html',
                          {'comments': list_comments,
                           'teacher_lesson': obj_teacher_lesson,
                           'id': xid,
                           'hot': "{0:.1f}".format(hot),
                           'kind': kind,
                           'log_in': True,
                           'username': username,
                           })
        else:
            username = request.user.username
            obj_teacher_lesson = LessonTeacher.objects.get(id=request.POST['id'])  # 得到这门课程的信息
            xid = request.POST['id']
            return render(request, 'teacher_user.html',
                          {'teacher_lesson': obj_teacher_lesson,
                           'id': xid,
                           'kind': kind,
                           'log_in': True,
                           'username': username,
                           })
