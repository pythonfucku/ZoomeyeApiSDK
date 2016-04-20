#!/bin/env python 
# -*- coding: utf-8 -*-
import sys
from zoomeye.ZoomeyeApiSdk import ZoomeyeSDK

user = "your login name"
passwd = "your login passwd"
app = ZoomeyeSDK(user,passwd)

#设置高级搜索参数,webSearch或者hostSearch以后，被清空
app.advancedSearchArgs.os = "FreeBSD"
app.advancedSearchArgs.apple= "balalalala"
#app.advancedSearchArgs.app = "apple"

#先登录api
app.login()
#print app.access_token

#获取用户信息
app.resourcesInfo()

#搜索主机,返回全信息
result = app.hostSearch("cms",facets="os",page=1)

#获取搜索到的IP地址
print app.getIp_ZoomeyeSearch(result)

#搜索web，返回全信息
result = app.webSearch("cms",facets="os",page=1)

#获取搜索到的IP地址
print app.getIp_ZoomeyeSearch(result)

#获取搜索的总数
print app.total_ZoomeyeSearch(result)
