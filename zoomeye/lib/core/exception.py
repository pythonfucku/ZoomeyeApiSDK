#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:liangrt
Date:2016-03-10
"""

class ZoomeyeBaseException(Exception):
	pass

class ZoomeyeDataException(ZoomeyeBaseException):
	pass

class ZoomeyeClientResponsesException(ZoomeyeBaseException):
	pass

class ZoomeyeServerResponsesException(ZoomeyeBaseException):
	pass
