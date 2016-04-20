# ZoomeyeApiSDK
zoomeye api sdk base on python

zoomeye api sdk 提供了6中接口：
    login()
    说明：zoomeye api 登录接口，所有操作都需要先登录
    返回值：无
    
    
    resourcesInfo()
    说明：查询登陆者信息接口。
    返回值：{"plan": "developer", "resources": {"host-search": 9, "web-search": 40}}
    
    
hostSearch(query="",facets=None,page=1)
webSearch(query="",facets=None,page=1)
getIp_ZoomeyeSearch(searchResult)
total_ZoomeyeSearch(searchResult)
