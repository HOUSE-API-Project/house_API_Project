#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from requests.auth import HTTPBasicAuth
import dhtreader

type = 22
pin = 27

dhtreader.init()
t, h = dhtreader.read(type, pin)
humidity = "%2.2f" % (h)
basicID  = 'BASICID'
basicPASS  = 'BASICPASS'



url       = 'http://133.242.144.202/post'
auth      = HTTPBasicAuth(basicID, basicPASS)
headers   = {'content-type': 'application/json'}
json_data = {"humidity":humidity}
tag       = "shibuhouse.1f.humidity"
data      = json.dumps(json_data)
param     = {'tag':tag, 'data':data}
r = requests.post(url, params=param, headers=headers, auth=auth)