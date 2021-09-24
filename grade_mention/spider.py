import requests
from .grade import Semester


def login(session, username, password):
    loginurl = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fjw.ustc.edu.cn%2Fucas-sso%2Flogin'
    formdata = {'model': 'uplogin.jsp', 'service': 'https://jw.ustc.edu.cn/ucas-sso/login',
                'username': username, 'password': password}
    session.post(loginurl, data=formdata)


def get_grade(username, password):
    session = requests.session()
    login(session, username, password)
    grade_sheet = session.get('https://jw.ustc.edu.cn/for-std/grade/sheet/getGradeList?trainTypeId=1&semesterIds').json()
    semester_dict = {str(sem['id']): Semester(**sem) for sem in grade_sheet['semesters']}
    return grade_sheet['overview'], semester_dict
