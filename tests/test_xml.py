import xmltodict
import json

DATA = b'<xml><ToUserName><![CDATA[gh_96c685096fbd]]></ToUserName>\n<FromUserName><![CDATA[ok6iXw0TuofZb99-CDNej_f6Zpio]]></FromUserName>\n<CreateTime>1500455396</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n<Content><![CDATA[1]]></Content>\n<MsgId>6444406855528347691</MsgId>\n</xml>'

if __name__ == '__main__':
    res = xmltodict.parse(DATA.decode(),process_namespaces=True)
    print(json.loads(json.dumps(res)))
    j = json.loads(json.dumps(res))
    res = xmltodict.unparse(j)
    print(res)
    # print(res,type(res))
    # print(dict(res))
    # print(res['ToUserName'])
    # print(type(DATA.decode()))