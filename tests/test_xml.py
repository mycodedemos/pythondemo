import xmltodict
import json

DATA = b'<xml><ToUserName><![CDATA[gh_96c685096fbd]]></ToUserName>\n<FromUserName><![CDATA[ok6iXw0TuofZb99-CDNej_f6Zpio]]></FromUserName>\n<CreateTime>1500455396</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n<Content><![CDATA[1]]></Content>\n<MsgId>6444406855528347691</MsgId>\n</xml>'
DATA = """
<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>2</ArticleCount>
<Articles>
<item>
<Title><![CDATA[title1]]></Title>
<Description><![CDATA[description1]]></Description>
<PicUrl><![CDATA[picurl]]></PicUrl>
<Url><![CDATA[url]]></Url>
</item>
<item>
<Title><![CDATA[title]]></Title>
<Description><![CDATA[description]]></Description>
<PicUrl><![CDATA[picurl]]></PicUrl>
<Url><![CDATA[url]]></Url>
</item>
</Articles>
</xml>"""
if __name__ == '__main__':
    res = xmltodict.parse(DATA,process_namespaces=True)
    print(json.loads(json.dumps(res)))
    j = json.loads(json.dumps(res))
    res = xmltodict.unparse(j)
    print(res)
    # print(res,type(res))
    # print(dict(res))
    # print(res['ToUserName'])
    # print(type(DATA.decode()))