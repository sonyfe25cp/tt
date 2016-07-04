# coding=utf-8
__author__ = 'omar'
import sys

import web

from datafetcher import parse_all_details
from analysis import HawkEye


urls = (
    '/', 'index',
    '/a', 'aaa',
    '/cs', 'cs'

)

render = web.template.render('templates/')

folder_path = '../data/papers'
all_paper_details = parse_all_details(folder_path)  # fetch all
print 'all_paper_details length:', len(all_paper_details)
he = HawkEye(all_paper_details)


class index:
    def GET(self):
        pass

        # school_meta_map = he.desc_all()

        # map = {}
        # for key in map.keys()

        school_meta_map = {'a':'b'}

        name = 'Bob'
        return render.index(school_meta_map)


class cs:
    def GET(self):
        pass
        # df = self.papers_df
        # df = df[df['school'] == school_name]
        school_meta = he.desc_school(u'计算机学院', None)
        return render.cs(school_meta)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app = web.application(urls, globals())
    app.run()

