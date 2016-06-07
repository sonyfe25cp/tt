# coding=utf-8
__author__ = 'omar'


class Paper:
    paper_id = ''
    title = ''
    author = ''
    mentor = ''
    student_id = ''
    major_type = 0
    defence_date = ''

    def __init__(self, paper_id, title, author, mentor, student_id, major_type, defence_date):
        self.paper_id = paper_id
        self.title = title
        self.author = author
        self.mentor = mentor
        self.student_id = student_id
        self.major_type = major_type
        self.defence_date = defence_date




