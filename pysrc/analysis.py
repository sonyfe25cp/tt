# coding=utf-8
__author__ = 'omar'

import pandas as pd


class HawkEye:
    papers_df = None

    _degree_array = []
    _major_first_array = []
    _open_status_array = []
    _school_array = []

    def __init__(self, papers):
        columns = ['paper_id', 'title', 'student_id', 'author',
                   'degree', 'school', 'mentor', 'mentor_school',
                   'major_first', 'major', 'paper_abstract', 'open_status',
                   'major_type', 'defence_date', 'keywords']
        datas = []
        for paper in papers:
            raw_row = []
            raw_row.extend([paper.paper_id, paper.title, paper.student_id, paper.author,
                            paper.degree, paper.school, paper.mentor, paper.mentor_school,
                            paper.major_first, paper.major, paper.paper_abstract, paper.open_status,
                            paper.major_type, paper.defence_date, paper.keywords])
            datas.append(raw_row)
        self.papers_df = pd.DataFrame(datas)
        self.papers_df.columns = columns
        # print '------------------'
        # print papers_df.head(10)
        # print '------------------'
        self._degree_array = self.papers_df['degree'].unique()
        self._major_first_array = self.papers_df['major_first'].unique()
        self._open_status_array = self.papers_df['open_status'].unique()
        self._school_array = self.papers_df['school'].unique()

    def desc(self):
        print 'degrees:'
        for degree in self._degree_array:
            print degree
        print 'major_first'
        for major_first in self._major_first_array:
            print major_first
        print 'school:'
        for school in self._school_array:
            print school
        print 'open_status:'
        for open_status in self._open_status_array:
            print open_status

    def desc_school(self, school_name):
        df = self.papers_df
        df = df[df['school'] == school_name]
        degrees = df['degree'].unique() #degree
        mentors = df['mentor'].unique() #mentors

        desc_array(degrees)
        desc_array(mentors)

    def desc_mentor(self, school_name, mentor_name):
        df = self.papers_df
        df = df[df['school'] == school_name][df['mentor'] == mentor_name]
        df = df.groupby('degree')
        print df.head()



def desc_array(array):
        for ar in  array:
            print ar
