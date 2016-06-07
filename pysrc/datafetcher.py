# coding=utf-8
__author__ = 'omar'
import urllib
import codecs

import requests
from paper import Paper
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import sys
import os
from time import time



def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


html = getHtml("http://tieba.baidu.com/p/2738151262")


def fetch_list():
    base_url = 'http://10.1.123.249/xwlw/system/DataSource/GetDataGridCtrlResult.aspx?_debug_=undefined'
    init = 0
    pageSize = 35000
    # pageSize = 500
    begin = init * pageSize
    req_data = '''<Root><A3020>system</A3020><A3001>se║lect LT_PaperBase.RUID,LT_PaperBase.subject,LT_PaperBase.name,LT_PaperBase.tutorName1,LT_PaperBase.listry,LT_PaperBase.degree,LT_PaperBase.replyDate FROM LT_PaperBase where LT_PaperBase.audit = '审核合格' AND replydate &gt;='2000-1-1' and replydate &lt;= '2016-06-07' order by REPLYDATE DESC</A3001><A3002 valueType="4">''' \
               + str(begin) + '</A3002><A3003 valueType="4">' + str(pageSize) + '</A3003></Root>'''

    # req = urllib2.urlopen(base_url, post_params)
    # content = req.read()
    # print content

    response = requests.post(base_url, data=req_data)
    # print response.text
    text = response.text
    print len(text)

    f = codecs.open("../data/list.xml", "w", "utf-8")
    f.write(text)
    f.close()


def fetch_details(paper_id):
    details_url = 'http://10.1.123.249/xwlw/system/datasource/selectrecordset.aspx'
    req_data = "<Root><A3020>system</A3020><A3001>se║lect LT_PaperBase.abstract1,LT_PaperBase.subject,LT_PaperBase.science,LT_PaperBase.degree,LT_PaperBase.replyDate,LT_PaperBase.secret,LT_PaperBase.foreignSubject,LT_PaperBase.tutorName1,LT_PaperBase.tutorUnits1,LT_PaperBase.tutorName2,LT_PaperBase.tutorUnits2,LT_PaperBase.length,LT_PaperBase.referLength,LT_PaperBase.abstract2,LT_PaperBase.research,LT_PaperBase.country,LT_PaperBase.audit,LT_PaperBase.views,LT_PaperBase.listing,LT_PaperBase.school,LT_PaperBase.scanNumber,LT_PaperBase.schoolID,LT_PaperBase.keyword2,LT_PaperBase.tutorname3,LT_PaperBase.tutorunits3,LT_PaperBase.name,LT_PaperBase.college1,LT_PaperBase.professname,LT_PaperBase.refer,LT_PaperBase.listry,LT_PaperBase.RUID,LT_PaperBase.keyword1,LT_PaperBase.paperState,LT_PaperBase.PERMISSIONTYPE,LT_PaperBase.STATEFLAG,r152f3c840006dec351.name AS _102c9401000086XXXX_0,r152f3c850006dfc351.RESNAME AS _10c6c679000016XXXX_1,r152f3c850006e0c351.RESNAME AS _102aef92000048XXXX_2,r152f3c850006e1c351.RESNAME AS _119ebc470009c6c351_3 FROM LT_PaperBase LEFT OUTER JOIN LT_BASENEWS r152f3c840006dec351 ON LT_PaperBase.degree = r152f3c840006dec351.code LEFT OUTER JOIN PT_RESOURCETYPEBASE r152f3c850006dfc351 ON LT_PaperBase.college1 = r152f3c850006dfc351.RUID LEFT OUTER JOIN PT_RESOURCERE1 r152f3c850006e0c351 ON LT_PaperBase.science = r152f3c850006e0c351.RESOURCEID LEFT OUTER JOIN PT_RESOURCERE1 r152f3c850006e1c351 ON LT_PaperBase.professname = r152f3c850006e1c351.RESOURCEID WHERE LT_PaperBase.RUID = '" + paper_id + "'</A3001><A3002 valueType=\"4\">0</A3002><A3003 valueType=\"4\">1</A3003></Root>"

    response = requests.post(details_url, data=req_data)
    text = response.text
    # print text
    # print len(text)
    f = codecs.open("../data/papers/" + paper_id + ".xml", "w", "utf-8")
    f.write(text)
    f.close()

def parse_list(file_path):
    papers = []
    try:
        tree = ET.parse(file_path)  # 打开xml文档
        root = tree.getroot()  # 获得root节点
        n_parent = root.findall('N23008')[0]
        for node_group in n_parent.findall('N23008'):
            attributes = node_group.findall('A3015')
            paper_id = attributes[0].text
            title = attributes[1].text
            author = attributes[2].text
            mentor = attributes[3].text
            student_id = attributes[4].text
            major_type = attributes[5].text
            defence_date = attributes[6].text
            # print paper_id, title, author, mentor, student_id, major_type, defence_date
            paper = Paper(paper_id, title, author, mentor, student_id, major_type, defence_date)
            papers.append(paper)
    except Exception, e:
        print e
        print root.tag, "---", root.attrib
    return papers

def fetch_paper_details(papers):
    papers_folder = os.listdir('../data/papers')
    print 'there are', len(papers), 'papers need to fetch'
    print 'i have fetched', len(papers_folder), 'papers'
    print len(papers) - len(papers_folder), 'need to finish'
    i = 0
    t0 = time()
    for paper in papers:
        paper_id = paper.paper_id
        file_name = paper_id+".xml"
        if file_name not in papers_folder:
            # print 'fetching ' + paper_id
            fetch_details(paper_id)
            i += 1
            if i % 100 == 0:
                print 'have fetched', str(i), 'papers, cost', time()-t0, 's'
    print i

if __name__ == '__main__':
    # fetch_list()
    # fetch_details('1d1af609000021c351')
    # papers = parse_list("../data/list_sample.xml")
    papers = parse_list("../data/list.xml")
    fetch_paper_details(papers)

