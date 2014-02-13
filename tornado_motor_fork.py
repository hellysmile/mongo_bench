#!/usr/bin/env python
import tornado.web
import tornado.ioloop
import tornado.httpserver
import motor


class IndexRequestHandler(tornado.web.RequestHandler):
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = motor.MotorClient().open_sync()['documents']

        return self._db

    @tornado.web.asynchronous
    def get(self):
        self.db.items.find_one(
            {},
            callback=self._on_find_one
        )

    def _on_find_one(self, result, error):
        self.write(result['data'])
        self.finish()


if __name__ == '__main__':
    application = tornado.web.Application(
        [
            (r'/', IndexRequestHandler)
        ]
    )

    server = tornado.httpserver.HTTPServer(application)
    server.bind(7777)
    server.start(2)

    tornado.ioloop.IOLoop.instance().start()
