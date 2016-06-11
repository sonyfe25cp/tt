# coding=utf-8
__author__ = 'omar'


class Paper:
    paper_id = ''
    paper_abstract = ''
    title = ''
    author = ''
    mentor = ''
    mentor_school = ''
    student_id = ''
    major_first = ''
    major = ''
    open_status = ''
    major_type = 0
    defence_date = ''
    keywords = ''
    degree = ''
    school = ''

    def __init__(self):
        return

    def __init__(self, paper_id, title, author, mentor, student_id, major_type, defence_date):
        self.paper_id = paper_id
        self.title = title
        self.author = author
        self.mentor = mentor
        self.student_id = student_id
        self.major_type = major_type
        self.defence_date = defence_date

    def __init__(self, paper_id, paper_abstract, title, author, mentor, mentor_school, student_id, major_first,
                 major, open_status, major_type, defence_date, keywords, degree, school):
        self.paper_id = paper_id
        self.paper_abstract = paper_abstract
        self.title = title
        self.author = author
        self.mentor = mentor
        self.mentor_school = mentor_school
        self.student_id = student_id
        self.major_first = major_first
        self.major_type = major_type
        self.major = major
        self.open_status = open_status
        self.defence_date = defence_date
        self.keywords = keywords
        self.degree = degree
        self.school = school

    def __repr__(self):
        return '''%s\t%s''' % (self.paper_id, self.paper_abstract)

    def __str__(self):
        return '''paper_id', %s
        'paper_abstract', %s
        'title', %s
        'major_first', %s
        'major', %s
        'open_status', %s
        'mentor', %s
        'mentor_school', %s
        'author', %s
        'student_id', %s
        'key_words', %s
        'degree', %s
        'school', %s''' % (
            self.paper_id, self.paper_abstract, self.title, self.major_first, self.major, self.open_status, self.mentor,
            self.mentor_school, self.author, self.student_id, self.keywords, self.degree, self.school)
