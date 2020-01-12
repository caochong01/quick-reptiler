# -*- coding: utf-8 -*-
"""
    # HTTP报文解析工具
    # 报文自动请求、报文提取器（method、url、head、body）、报文填充返回填充报文
"""
import re
import requests
import copy

from bhcrjyApp.settings import URL_PREFIX


class HTTPMessage(object):
    """
    HTTP报文解析器，提供HTTP报文处理的方法和能力
    同时提供了报文缓存，请使用本包外部变量 http_message获取
    """
    __cacheMessage = {}

    def readMessageFile(self, tag, uri, coding='utf-8'):
        """
        读取文件的报文，解析后缓存
        :return: RequestBody对象
        """
        message = None
        with open(uri, mode='r', encoding=coding) as f:
            start = F'#:{tag}:#'
            stop = F'##:{tag}:##'
            pattern = F'{start}(.*?){stop}'
            # match = re.match(pattern, f.read(), re.S)
            # if match:
            #     print(match.group(0))
            pat = re.compile(pattern, re.S)
            result = pat.findall(f.read())
            for q in result:
                message = self.parserMessage(q.strip('\n'))

        if not self.__cacheMessage.get(tag, None):
            self.__cacheMessage[tag] = message
        return message

    def cacheMessage(self, tag, uri=None):
        """
        读取或者写入缓存，RequestBody对象
        （入口方法，不存在则直接读取文件）
        :return:
        """
        if not tag:
            return None

        message = self.__cacheMessage.get(tag, None)
        if message or uri is None:
            if message:
                return copy.deepcopy(message)
            return message
        else:
            message = self.readMessageFile(tag, uri)
            return copy.deepcopy(message)

    def parserMessage(self, message=None):
        """
        解析报文字符串
        :return: RequestBody对象
        """
        if message is None:
            return None

        num = 0
        req_body = RequestBody()
        for i in message.split('\n'):
            line = i.strip('\n')
            if num == 0:
                num += 1
                lineH = line.split(' ')
                if len(lineH) == 3:
                    req_body.method, req_body.url, req_body.http_version = lineH
                continue

            lineW = line.replace(' ', '').split(':')
            if len(lineW) == 2:
                key, value = lineW
                req_body.putHeader(key, value)

        return req_body


class RequestBody(object):
    """
    请求体对象的封装，可提供请求体的内容的灵活调取，
    请求头和请求体字段映射
    """
    method = None
    url = None
    http_version = None
    header = {}
    body = None

    def __init__(self, method='GET', url=None, http_version='HTTP/1.1', **header):
        """
        请求方法、请求路径、HTTP版本、请求头参数
        """
        self.method = method
        self.url = url
        self.http_version = http_version
        self.header = header

    def putBody(self, body):
        # TODO body可以接收字符串或者元组，需要优化
        if body:
            self.body = body
            # if type(body) is dict:
            #     self.body = body
            # else:
            #     raise Exception('The parameter should be dict type.')

    def putHeader(self, key, value):
        self.header[key] = value

    def proceUrl(self, mapping=None, prefix_c='[[', suffix_c=']]'):
        """
        URL参数的报文模板处理方法

        :param mapping: 模板映射参数
        :param prefix_c: RequestBody报文对象映射标识前缀
        :param suffix_c: RequestBody报文对象映射标识后缀
        :return: self
        """
        if mapping:
            for mkey, mvalue in mapping.items():
                self.url = self.url.replace(F'{prefix_c}{mkey}{suffix_c}', mvalue)
        return self

    def proceHead(self, mapping=None, is_param_mapping=True,
                  prefix_c='[[', suffix_c=']]'):
        """
        header参数的报文模板处理方法

        :param mapping: 模板映射参数
        :param prefix_c: RequestBody报文对象映射标识前缀
        :param suffix_c: RequestBody报文对象映射标识后缀
        :param is_param_mapping: 是否采用参数映射，而不是全字段映射（value的全替换）
        :return: self
        """
        if not mapping:
            return self

        if is_param_mapping:
            headers = self.header
            for key, value in headers.items():
                for mkey, mvalue in mapping.items():
                    value = value.replace(F'{prefix_c}{mkey}{suffix_c}', mvalue)

                self.header[key] = value
        else:
            self.header.update(mapping)
        return self

    def proceBody(self, mapping=None, is_param_mapping=False,
                  prefix_c='[[', suffix_c=']]'):
        """
        body参数的报文模板处理方法

        :param mapping: 模板映射参数
        :param prefix_c: RequestBody报文对象映射标识前缀
        :param suffix_c: RequestBody报文对象映射标识后缀
        :param is_param_mapping: 是否采用参数映射，而不是全字段映射（value的全替换）
        :return: self
        """
        if not mapping:
            return self

        if is_param_mapping:
            bodys = self.body
            for key, value in bodys.items():
                for mkey, mvalue in mapping.items():
                    value = value.replace(F'{prefix_c}{mkey}{suffix_c}', mvalue)

                self.body[key] = value
        else:
            self.body.update(mapping)
        return self


class HttpUtils(object):
    """
    GET、POST请求封装，
    """

    def get(self, url, params=None, **kwargs):
        """
        requests框架的原生 get请求

        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        with requests.get(url, params=params, **kwargs) as resp:
            response = resp
        return response

    def post(self, url, data=None, json=None, **kwargs):
        """
        requests框架的原生 post请求

        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        with requests.post(url, data=data, json=json, **kwargs) as resp:
            response = resp
        return response

    @classmethod
    def request(cls, tag=None, uri=None, body=None, request_body=None,
                mapping=None, is_param_mapping=True,
                prefix_c='[[', suffix_c=']]', **kwargs):
        """
        根据报文自动发起 GET、POST请求
        如果不能满足您的一般需求，请使用get、post方法
        注：如果 kwargs参数设定了cookies，当请求头中有Cookie时，参数不生效（requests源码解释）

        :param body: get或者 post请求参数
        :param prefix_c: RequestBody报文对象映射标识前缀
        :param suffix_c: RequestBody报文对象映射标识后缀
        :param mapping: RequestBody报文对象的映射字典对象
        :param is_param_mapping: 是否采用参数映射，而不是全字段映射

        :param tag: 通过 tag来读取本地缓存的 RequestBody报文对象
        :param uri: 原始报文文件位置，如果根据 tag查找本地缓存不存在，则会检索该文件
        :param request_body: 一个完整的 RequestBody报文对象
        :param kwargs: :class:`requests.request` method
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        if request_body is None:
            request_body = http_message.cacheMessage(tag, uri=uri)
            if request_body is None:
                return None
            request_body.proceUrl(mapping, prefix_c, suffix_c) \
                .proceHead(mapping, is_param_mapping, prefix_c, suffix_c) \
                .proceBody(mapping, is_param_mapping, prefix_c, suffix_c) \
                .putBody(body)

        if request_body.method.upper() == 'POST':
            return cls().post(URL_PREFIX + request_body.url,
                              data=request_body.body,
                              headers=request_body.header,
                              **kwargs)
        else:
            return cls().get(URL_PREFIX + request_body.url,
                             params=request_body.body,
                             headers=request_body.header,
                             **kwargs)


http_message = HTTPMessage()
