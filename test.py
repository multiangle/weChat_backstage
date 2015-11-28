__author__ = 'multiangle'
import tornado.web
import tornado.ioloop
import tornado.options
import time

from xml.etree.ElementTree import  Element,SubElement,Comment,tostring
import xml.etree.ElementTree as etree

from tornado.options import define,options
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
        # ret_data={}
        # ret_data['ToUserName']=dict_data['FromUserName']
        # ret_data['FromUserName']=dict_data['ToUserNamee']
        # ret_data['CreateTime']=str(int(time.time()))
        # ret_data['MsgType']='text'
        # ret_data['Content']='hehehe'
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

if __name__=='__main__':
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
