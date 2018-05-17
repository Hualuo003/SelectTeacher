#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import imp

# imp.reload(sys)
# sys.setdefaultencoding("utf-8")

sys.path.append('../')
from config import configs
from model import model
import web
import util
from model.orm import *
from config_default import remind_source
from config_default import exampage_source
import time

urls = (
    'Login', 'Login',
    'GetTeacher', 'GetTeacher',
    'SelectTeacher', 'SelectTeacher',
    'AddTeacher', 'AddTeacher',
    'DeleteTeacher', 'DeleteTeacher',
    'print_exam', 'print_exam',
    'BatchPrintExam', 'BatchPrintExam',
    'Remind', 'Remind',
    'SaveRemind', 'SaveRemind',
)


class BatchPrintExam:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        params = web.input()
        # class Params:
        #     def __init__(self):
        #         self.class_cl_id = 2
        #         self.ex_id = 2
        #
        # params = Params()

        class_ = model.Class_model.getByPK(params.class_cl_id)
        exam = model.Exam_model.getByPK(params.ex_id)
        ex, cl = exam.ex_id, class_.cl_id
        ex_cl = '%s_%s' % (ex, cl)
        examDir  = '%s/%s' % (exampage_source, ex_cl)
        try:
            os.mkdir(examDir)
        except:
            shutil.rmtree(examDir)
            os.mkdir(examDir)
        try:
            student = model.Student_has_class_model.getByArgs(class_cl_id=params.class_cl_id)
            for student_id in student:
                filepath = examDir + '/%s.docx' % (student_id.student_st_id)
                print(filepath)
                util.word(student_id.student_st_id, params.ex_id, filepath)
            zip_path = '/source/exampage/%s.zip' % (ex_cl)
            util.zip_path(examDir,
                          '%s' % (exampage_source),
                          '%s.zip' % (ex_cl))
        except:
            print("e")
            response = util.Response(status=util.Status.__error__, )
            return util.objtojson(response)
        response = util.Response(status=util.Status.__success__, message=zip_path)
        return util.objtojson(response)

        # try:
        #     os.mkdir('%s/%s_%s' % (exampage_source, params.class_cl_id, params.ex_id))
        # except:
        #     shutil.rmtree('%s/%s_%s' % (exampage_source, params.class_cl_id, params.ex_id))
        #     os.mkdir('%s/%s_%s' % (exampage_source, params.class_cl_id, params.ex_id))
        # try:
        #     student = model.Student_has_class_model.getByArgs(class_cl_id=params.class_cl_id)
        #     for student_id in student:
        #         filepath = str(
        #             '%s/%s_%s/%s.docx' % (exampage_source, params.class_cl_id, params.ex_id, student_id.student_st_id))
        #         # print filepath
        #         util.word(student_id.student_st_id, params.ex_id, filepath)
        #     zip_path = str('/source/exampage/%s_%s.zip' % ( params.class_cl_id, params.ex_id))
        #     util.zip_path('%s/%s_%s' % (exampage_source, params.class_cl_id, params.ex_id), '%s' % (exampage_source),
        #                   u'%s_%s.zip' % (params.class_cl_id, params.ex_id))
        # except:
        #     response = util.Response(status=util.Status.__error__,)
        #     return util.objtojson(response)
        # response = util.Response(status=util.Status.__success__, message =zip_path)
        # return util.objtojson(response)


if __name__ == '__main__':
    bat = BatchPrintExam()
    bat.POST()


class print_exam:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        # 接收参数
        params = web.input()
        # session = web.ctx.session
        # session.student_id = params.student_id
        # session.ex_id = params.ex_id
        response = util.Response(status=util.Status.__success__, )
        return util.objtojson(response)


class DeleteTeacher:
    def POST(self):
        print("删除教师信息")
        web.header("Access-Control-Allow-Origin", "*")
        # 接收参数
        params = web.input()
        print(params)
        teacher = model.Teacher_model(**params)
        if teacher.delete():
            response = util.Response(status=util.Status.__success__, )
            return util.objtojson(response)
        else:
            response = util.Response(status=util.Status.__error__, )
            return util.objtojson(response)


class AddTeacher:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        # 接收参数
        params = web.input()
        print(params)
        teacher = model.Teacher_model(**params)
        if teacher.insert():
            response = util.Response(status=util.Status.__success__, )
            return 1
        else:
            response = util.Response(status=util.Status.__error__, )
            return 0


class Login:
    def GET(self):
        return web.seeother('/static/TeacherLogin.html', True)

    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        # 接收参数
        params = web.input()
        # session = web.ctx.session
        teacher = model.Teacher_model.getByArgs(tc_id=params.tc_id)
        print(teacher)
        # util.getFileRotatingLog().debug(params)
        if teacher[0].tc_password != params.password:
            response = util.Response(status=util.Status.__error__, message="密码错误")
            return util.objtojson(response)
        else:
            # session.username = params.tc_id
            response = util.Response(status=util.Status.__success__, )
            return util.objtojson(response)


class GetTeacher:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        # 接收参数
        params = web.input()
        try:
            # session = web.ctx.session
            # username = ""
            if not username:
                print("not login")
                response = util.Response(status=util.Status.__not_login__, message='4')
                return util.objtojson(response)
        except Exception as e:
            print(e)
            response = util.Response(status=util.Status.__not_login__, message='4')
            return util.objtojson(response)
        teacher = model.Teacher_model.getByArgs(tc_id=session.username)
        if teacher[0].tc_level == '管理员':
            response = util.Response(status=util.Status.__success__, message='1')
            return util.objtojson(response)
        else:
            response = util.Response(status=util.Status.__success__, message='2')
            return util.objtojson(response)


class SelectTeacher:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        # 接收参数
        teacher = model.Teacher_model.query('select * from teacher')
        teacher = [model.Teacher_model(**item) for item in teacher]
        response = util.Response(status=util.Status.__success__, body=teacher)
        print(util.objtojson(response))
        return util.objtojson(response)


class Remind:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        f = open('%s/remind.txt' % (remind_source), 'r')
        message = f.read()
        f.close()
        response = util.Response(status=util.Status.__success__, message=message)
        return util.objtojson(response)


class SaveRemind:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        params = web.input()
        f = open('%s/remind.txt' % (remind_source), 'w')
        f.write(params.remind)
        f.close()
        response = util.Response(status=util.Status.__success__, )
        return util.objtojson(response)


app = web.application(urls, globals())
render = web.template.render('template')
# if __name__ == '__main__':
#     if len(urls) & 1 == 1:
#         print "urls error, the size of urls must be even."
#     else:
#         app.run()
