# -*- coding: utf-8 -*-


class HttpCookies(object):
    __COOKIES = {}

    def get_cookie(self, key):
        return self.__COOKIES.get(key, None)

    def set_cookie(self, kv=None, **dicts):
        if kv is not None:
            if type(kv) is dict:
                self.__COOKIES.update(kv)

        if len(dicts):
            self.__COOKIES.update(dicts)

    def __getitem__(self, item):
        return self.__COOKIES.get(item, None)

    def __setitem__(self, key, value):
        self.__COOKIES[key] = value

    def __delitem__(self, key):
        self.__COOKIES.pop(key, None)


httpCookies = HttpCookies()

# Example code:
# httpCookies.set_cookie({'hello': 'world'})
# httpCookies.set_cookie(hellos={'123': '456'})
# httpCookies['hello'] = '45689'
# del httpCookies['hello']
# print(httpCookies['hello'])
