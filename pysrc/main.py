# coding=utf-8
__author__ = 'omar'
import web

urls = (
    '/', 'index',
    '/a', 'aaa'
)

render = web.template.render('templates/')
class index:
    def GET(self):
        name = 'Bob'
        return render.index(name)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

