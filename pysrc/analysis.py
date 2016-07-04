# coding=utf-8
__author__ = 'omar'
import re

import pandas as pd

from school_meta import School_meta


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
        self.papers_df['start_year'] = compute_start_year_from_sutdent_id(paper.student_id)
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


    def desc_all(self):
        df = self.papers_df
        df_schools = df.groupby('school')

        school_meta_map = {}

        for name, group in df_schools:
            print name, 'with', len(group), 'students'
            # print group
            school_meta = self.desc_school(name, group)
            print '-----------------------------------'
            school_meta_map[name] = school_meta
        return school_meta_map

    # df = self.papers_df
    # df = df[df['school'] == school_name]
    def desc_school(self, name, df_school):

        if df_school == None:
            df_school = self.papers_df[self.papers_df['school'] == name]

        school_meta = School_meta()
        school_meta.name = name
        school_meta.student_count = len(df_school)

        degrees = df_school['degree'].unique()  # degree
        mentors = df_school['mentor'].unique()  # mentors

        df_school_degrees = df_school.groupby('degree')
        for name, degree_group in df_school_degrees:
            print name, ':', len(degree_group)
            school_meta.degrees_map[name] = len(degree_group)
        # df_school_degrees['']

        df_school_mentors = df_school.groupby('mentor')
        for name, mentor_group in df_school_mentors:
            print name, 'has', len(mentor_group), 'students'
            school_meta.mentors_map[name] = len(mentor_group)

        return school_meta


    # df = self.papers_df
    # df = df[df['school'] == school_name][df['mentor'] == mentor_name]
    def desc_mentor(self, df_mentor):
        df_mentor_degrees = df_mentor.groupby('degree')
        # print df.head()
        for name, mentor_degree in df_mentor_degrees:
            print name, ':', len(mentor_degree)


def compute_start_year_from_sutdent_id(student_id):
    if re.match(r"^[12](\d{2})\d{5}", student_id):
        return '20' + student_id[1:3]
    elif re.match(r"3\d{3}(\d{2})\d{4}", student_id):
        return '20' + student_id[4:6]
    else:
        return None


if __name__ == '__main__':
    array = ['020928', '0ZZ02862', '10201024', '10201026', '20301406', '20301393', '3120100392']
    for a in array:
        print a, ' ==> ', compute_start_year_from_sutdent_id(a)


def desc_array(array):
    for ar in array:
        print ar
    print '************************'