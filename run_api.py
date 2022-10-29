import json
import os

import swagger_ui
import yaml
import tornado.httpserver
import tornado.ioloop
from datetime import datetime
from tornado.web import RequestHandler
from db_init import Database


db = Database()


with open("configs/config.yaml", "r") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


class BaseHandler(RequestHandler):
    """Base class for handlers"""

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def json_response(self, status, data):
        """Helper method for sending response containing json data
        """
        self.set_header("Content-Type", "application/json")
        self.set_status(status)
        self.write(json.dumps(data))

    def data_received(self, chunk: bytes) -> None:
        pass


class DataHandler(BaseHandler):
    """Handler for user data request"""
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    """Get method for providing data to the user"""
    def get(self):
        if not self.current_user:
            self.json_response(403, {"success": False,
                                     "message": "Not Authorized"})
        else:
            data = db.get_table_data()
            self.write(json.dumps(data, ensure_ascii=False))
            db.update_user_request_time(datetime.utcnow())


class AuthHandler(BaseHandler):
    """Handler for user authorization request"""
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self):
        """Post method for authorization"""

        payload = json.loads(self.request.body)
        login = payload.get("login")
        password = payload.get("password")
        created_at = datetime.utcnow()
        if not (login and password):
            self.json_response(400, {"success": False,
                                     "message": "Bad request"})
            return

        user_exist = db.is_user_exist(login)
        if user_exist:
            if not db.check_password(login, password):
                self.json_response(401, {"success": False,
                                         "message": "Wrong password"})

                self.clear_cookie("user")
                return
        else:
            db.insert_user_to_db(login, password, created_at)

        self.set_secure_cookie("user", login)
        self.json_response(200, {"success": True, "login": login})


def make_app():
    settings = dict(
        cookie_secret=str(os.urandom(45)),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        xsrf_cookies=False,
    )

    handlers = [
        (r"/api/data", DataHandler),
        (r"/api/login", AuthHandler)
    ]

    application = tornado.web.Application(handlers, **settings)

    swagger_ui.tornado_api_doc(
        application,
        config_path='./swagger.json',
        url_prefix="/swagger",
        title="Tornado API",
    )

    http_server = tornado.httpserver.HTTPServer(application)
    port = cfg['server']['port']
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    make_app()
