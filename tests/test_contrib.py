# -*- coding: utf-8 -*-

import os
import time
import random
from werobot.utils import generate_token, get_signature
import sys


def test_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "django_test.settings")
    sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../werobot/tests/contrib/django_test/'))

    from django.test.utils import setup_test_environment
    setup_test_environment()
    from django.test.client import Client
    from werobot.parser import parse_xml, process_message
    import django

    django.setup()

    c = Client()

    token = 'TestDjango'
    timestamp = str(time.time())
    nonce = str(random.randint(0, 10000))
    signature = get_signature(token, timestamp, nonce)
    echostr = generate_token()

    response = c.get('/robot/', {'signature': signature,
                                 'timestamp': timestamp,
                                 'nonce': nonce,
                                 'echostr': echostr})
    assert response.status_code == 200
    assert response.content.decode('utf-8') == echostr

    xml = """
    <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[this is a test]]></Content>
        <MsgId>1234567890123456</MsgId>
    </xml>"""
    params = "?timestamp=%s&nonce=%s&signature=%s" % \
             (timestamp, nonce, signature)
    url = '/robot/' + params
    response = c.post(url,
                      data=xml,
                      content_type="text/xml")

    assert response.status_code == 200
    response = process_message(parse_xml(response.content))
    assert response.content == 'hello'
