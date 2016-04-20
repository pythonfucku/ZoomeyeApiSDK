#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:liangrt
Date:2016-03-30
"""

import json
import urllib

from zoomeye.thirdparty import requests
from zoomeye.lib.core.data import logger
from zoomeye.lib.core.datatype import AttribDict
from zoomeye.lib.core.enums import ZOOMEYEURL
from zoomeye.lib.core.enums import ZOOMEYE_ECODE
from zoomeye.lib.core.enums import ZOOMEYE_FACETS
from zoomeye.lib.core.enums import ZOOMEYE_ADVANCED_ARGS
from zoomeye.lib.core.exception import ZoomeyeBaseException
from zoomeye.lib.core.exception import ZoomeyeClientResponsesException
from zoomeye.lib.core.exception import ZoomeyeServerResponsesException

class ZoomeyeSDK():
	"""
	zoomeye api sdk
	"""
	def __init__(self,user,passwd):
		self.user = user
		self.passwd = passwd
		self.access_token = None
		self.header = None
		self.advancedSearchArgs = AttribDict()
		return

	def login(self):
		logger.info("zoomeye login is running")

		data = {
			"username" : self.user,
			"password" : self.passwd,
		}
		result = self._getRequests(ZOOMEYEURL.LOGINURL,data)
		self.access_token = result["access_token"]
		self.header = {'Authorization' : 'JWT ' + self.access_token,}
		#logger.debug("access_token:{0}".format(self.access_token))
		#logger.debug("header:{0}".format(self.header))
		logger.info("zoomeye login successful")

		self._checkZoomeyeKey()

	def resourcesInfo(self):
		logger.info("zoomeye recorces info is running")

		result = self._getRequests(ZOOMEYEURL.RESOURCESINFOURL)
		logger.info("zoomeye resource info:{0}".format(result))

	def hostSearch(self,query,facets=None,page=1):
		logger.info("zoomeye start searching host")
		query += self._setAdvancedSearchArgs()

		result = self._baseSearch(ZOOMEYEURL.HOSTSEARCHURL,ZOOMEYE_FACETS.HOST,query,facets,page)
		logger.info("zoomeye host request request count is {0}".format(len(result["matches"])))
		self._clearnAdvancedSearch()

		#TODO if result:result["matches"]

		return result
		
	def webSearch(self,query,facets=None,page=1):
		logger.info("zoomeye start searching web")
		query += self._setAdvancedSearchArgs()

		result = self._baseSearch(ZOOMEYEURL.WEBSEARCHURL,ZOOMEYE_FACETS.WEB,query,facets,page)
		logger.info("zoomeye web request request count is {0}".format(len(result["matches"])))
		self._clearnAdvancedSearch()

		#TODO if result:result["matches"]

		return result

	def getIp_ZoomeyeSearch(self,result):
		"""
		result:	result from webSearch or hostSearch
		return ip list
		"""
		ip_list = []
		if type(result) == dict:    
			if result.has_key("matches"):
				for x in result["matches"]:
					ip_list.append(x["ip"])
		return ip_list

	def total_ZoomeyeSearch(self,result):
		"""
		result: result from webSearch or hostSearch
		return result["total"] it's type is int,or 0
		"""
		if type(result) == dict:	
			if result.has_key("total"):
				return int(result["total"])
			else:
				errMessage = "result has no total key,set default 0"
				logger.error(errMessage)
		else:
			errMessage = "result type is not dict,input error"
			logger.error(errMessage)

		return 0


	def _baseSearch(self,url,facetEnums,query,facets,page):
		self._checkZoomeyeKey()
		page = self._checkArgumentsPage(page)
		facets = self._checkArgumentsFacets(facetEnums,facets)
		target = self._setTarget(url,query,facets,page)
		result = self._getRequests(target)
		return result

	def _getRequests(self,target,data=None):
		"""
		target:	target url
		data:	for post,if data is None,requests type is get 
		key:	return key's dict
		"""	
		try:
			if data:
				req = requests.post(target,data=json.dumps(data))
			else:
				req = requests.get(target,headers=self.header)	#TODO use many time
			info = json.loads(req.text)
			if not req.status_code in ZOOMEYE_ECODE.OK.keys():
				logger.error("zoomeye request error:{0}({1})".format(info["error"],req.status_code))
				logger.error(info["message"])
				raise ZoomeyeClientResponsesException(info["message"])
			else:
				return info
		except Exception as e:
			logger.error("zoomeye request error:{0}".format(str(e)))
			raise ZoomeyeClientResponsesException(str(e))

	def _setTarget(self,url,query,facets=None,page=1):
		if not facets:
			data = {
				"query" : query,
				"page" : page,
			}
		else:
			data = {
				"query" : query,
				"page" : page,
				"facet" : facets,
			}

		target = ("%s?%s") % (url,urllib.urlencode(data))

		logger.info("search target:{0}".format(target))
		return target

	def _checkArgumentsPage(self,page=None):
		if page:
			try:
				page = int(page)
			except:
				page = 1
		else:
			page = 1
		logger.debug("page:{0}".format(page))
		return page

	def _checkArgumentsFacets(self,facetEnums,facets):
		if not facets:
			return None

		if not type(facets) == list:
			facets = facets.split(",")
		facets = set(x.lower() for x in facets)

		total = set(facetEnums)
		tmp = facets & total
		if len(tmp) == 0:
			logger.error("facets can not accent:{0}".format(facets))
			logger.error("facets only can accent:{0}".format(total))
			logger.error("input facets error.")
			logger.info("set default facets empty.")
		elif len(tmp) < len(facets):
			logger.error("facets can not accent:{0}".format(facets - tmp))
			logger.error("facets only can accent:{0}".format(total))
			logger.info("set facets:{0}".format(tmp))
		facets = ",".join(tmp)

		logger.debug("facets:{0}".format(facets))
		return facets

	def _setHeader(self):
		self.header = {'Authorization' : 'JWT ' + self.access_token,}

	def _checkZoomeyeKey(self):
		if not self.access_token:
			errMessage = "zoomeye access_token is empty."
			logger.error(errMessage)
			raise ZoomeyeBaseException(errMessage)	
		if not self.header:
			errMessage = "zoomeye search header is empty."
			logger.error(errMessage)
			raise ZoomeyeBaseException(errMessage)	

	def _setAdvancedSearchArgs(self):
			"""
			参数可以是列表也可是字符串，但字符串必须以逗号或空格分割
			app:组件名包含
			ver:版本等于
			os:操作系统为
			country:国家为
			city:城市为
			device:设备类型为
			port:端口号为
			hostname:主机名包含
			services:服务类型为
			ip:IP 地址为
			cidr:IP 的 CIDR 网段
			site:域名包含
			desc:关键词包含
			keywords:描述包含
			"""
			tmp = ""
			flag = False
			for _ in self.advancedSearchArgs.items():
				if _[0] in ZOOMEYE_ADVANCED_ARGS.ARGS.keys():
					tmp += self._setAdvancedSearch(_[0],_[1])
					flag = True
				else:
					logger.error("zoomeye advanced search args type error(app.advancedSearchArgs.{0}=\"{1}\")".format(_[0],_[1]))
					logger.debug("you can use there args,like:")
					for x in ZOOMEYE_ADVANCED_ARGS.ARGS.items():
						logger.debug("{0}:{1}".format(x[0],x[1]))
					continue
			if not flag:
				logger.info("set advanced search args defalut(empty)")
			else:
				logger.info("zoomeye advanced search args[{0}]".format(tmp))
			return tmp

	def _setAdvancedSearch(self,name,arg):
		tmp = ""
		if not arg:
			return tmp

		if type(arg) == str:
			if ',' in arg:
				arg = arg.split(',')
			elif ' ' in arg:
				arg = arg.split(' ')
			else:
				tmp = " {0}:{1}".format(name,arg)
				return tmp
		elif type(arg) == list:
			pass
		else:
			errMessage = "setAdvancedSearch args type error"
			logger.error(errMessage)
			raise ZoomeyeBaseException(errMessage)
		for _ in arg:
			tmp += " {0}:{1}".format(name,_)
		return tmp


	def _clearnAdvancedSearch(self):
		self.advancedSearchArgs = AttribDict()






