__author__ = 'multiangle'

# import from tornado
import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define,options

# import from external libraries
import time
import json
import urllib.request as request
import requests
from xml.etree.ElementTree import  Element,SubElement,Comment,tostring
import xml.etree.ElementTree as etree

# import from this folder
from config import appid,appsecret


define('port',default=80,help='run on the given port',type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r'/',AuthHandler)
        ]
        settings=dict(
            debug=True
        )
        tornado.web.Application.__init__(self,handlers,**settings)

class AuthHandler(tornado.web.RequestHandler):
    def get(self):
        data=dict(
            signature=self.get_argument('signature'),
            timestamp=self.get_argument('timestamp'),
            nonce=self.get_argument('nonce'),
            echostr=self.get_argument('echostr')
        )
        self.write(data['echostr'])
        print(data)
        self.finish()
    def post(self):
        data={}
        print('hehe')
        xml_data=self.request.body
        print(xml_data)
        xml_data=str(xml_data,encoding='utf-8').replace('\n','')
        print(xml_data)
        xml_data=etree.fromstring(xml_data)
        dict_data=xml2dict(xml_data)

        if dict_data['MsgType']=='text':
            TEXT_MSG = u"""
<xml>
<ToUserName><![CDATA[{to_user_name}]]></ToUserName>
<FromUserName><![CDATA[{from_user_name}]]></FromUserName>
<CreateTime>{create_time}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
</xml>
"""
            output=TEXT_MSG.format(to_user_name=dict_data['FromUserName'],
                                from_user_name=dict_data['ToUserName'],
                                create_time=str(int(time.time())),
                                content='凑撒比'
                                )
            # output=bytes(output,encoding='utf-8')
            self.write(output)
            self.finish()
        if dict_data['MsgType']=='event':
            TEXT_MSG = u"""
<xml>
<ToUserName><![CDATA[{to_user_name}]]></ToUserName>
<FromUserName><![CDATA[{from_user_name}]]></FromUserName>
<CreateTime>{create_time}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
</xml>
"""
            output=TEXT_MSG.format(to_user_name=dict_data['FromUserName'],
                               from_user_name=dict_data['ToUserName'],
                               create_time=str(int(time.time())),
                               content='凑撒比'
            )
            # output=bytes(output,encoding='utf-8')
            self.write(output)
            self.finish()


def xml2dict(xml_data):
    dict_data={}
    len=xml_data.__len__()
    for i in range(len):
        if xml_data[i].__len__()>0:
            dict_data[xml_data[i].tag]=xml2dict(xml_data[i])
        else:
            dict_data[xml_data[i].tag]=xml_data[i].text
    return dict_data

def create_menu():
    access_token_url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}'.format(appid=appid,appsecret=appsecret)
    page=requests.get(access_token_url).content
    page=str(page,encoding='utf-8')
    page=json.loads(page)
    access_token=page['access_token']

    print(access_token)
    custom_menu=open('custom_menu','r')
    custom_menu=json.loads(custom_menu.read())
    create_menu_url='https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s'%(access_token)
    req=requests.post(create_menu_url,json=custom_menu)
    print(req.content)




if __name__=='__main__':
    # tornado.options.parse_command_line()
    # Application().listen(options.port)
    # tornado.ioloop.IOLoop.instance().start()
    create_menu()