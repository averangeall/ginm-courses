# -*- coding: utf8 -*-

import sys
import re
import models

def _get_one_course(line):
    line = re.sub(ur'[＊*]$', '', line)
    line = re.sub(ur'(基礎)|(進階)|(核心)|(專題)$', '', line)
    line = line.strip()
    mo = re.search(ur'\d+\s+([^\s\d]+)\s?(\d{3}\sU\d{3})?', line)
    assert mo
    course_name = mo.group(1)
    remain = line[len(mo.group()) :]
    mo = re.search(ur'((M|N|A)((，)(M|N|A))*)$', remain)
    assert mo
    course_discipline = mo.group(1).split(u'，')
    return (course_name, course_discipline)

def get_all_courses(fname):
    fr = open(fname)
    lines = fr.readlines()
    idx = 1
    courses = []
    for i, line in enumerate(lines):
        line = line.strip().decode('utf8')
        if line.startswith(str(idx)):
            back = lines[i + 1].strip().decode('utf8')
            line += back
            course = _get_one_course(line)
            courses.append(course)
            idx += 1
    return courses

def update_courses(fname):
    courses = get_all_courses(fname)
    models.Course.objects.all().delete()
    for course in courses:
        coursee = models.Course(name=course[0], discipline=','.join(course[1]))
        coursee.save()

