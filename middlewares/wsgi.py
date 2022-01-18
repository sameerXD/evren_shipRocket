class InterceptRequestMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        environ['HTTP_USER_AGENT'] = 'foobar'
        return self.wsgi_app(environ, start_response)