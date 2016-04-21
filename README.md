# Zoomeye Api SDK
zoomeye api sdk base on python

zoomeye api sdk 是基于python封装的zoomeye api。
zoomeye api官网说明：https://www.zoomeye.org/api


该SDK提供了6种接口：
    1.登录      [login()]
    2.查询用户信息      [resourcesInfo()]
    3.web搜索（高级）      
    4.host搜索（高级）
    5.过滤搜索IP
    6.获取搜索结果总数
    
    
接口说明：


    login()
    说明：zoomeye api 登录接口，所有操作都需要先登录
    返回值：无
    
    
    resourcesInfo()
    说明：查询登陆者信息接口。
    返回值：{"plan": "developer", "resources": {"host-search": 9, "web-search": 40}}
    
    
    hostSearch(query="",facets=None,page=1)
    说明：搜索主机
    参数：
        query：所要搜索的内容，不允许为空
        facets：要搜索的属性，可以为空，或者如下指定值：
            "app","device","service","os","port","country","city
        page：返回结果中的页数
    返回值：参见 https://www.zoomeye.org/api/doc#host-search
    
    
    webSearch(query="",facets=None,page=1)
    说明：搜索主机
    参数：
        query：所要搜索的内容，不允许为空
        facets：要搜索的属性，可以为空，或者如下指定值：
            "webapp","component","framework","frontend","server","waf","os","country","city"
        page：返回结果中的页数
    返回值： 参见 https://www.zoomeye.org/api/doc#web-search
        
        
    getIp_ZoomeyeSearch(searchResult)
    说明：从搜索结果中获取IP列表
    参数：hostSearch()的结果或者webSearch（）的结果
    返回值：IP列表
    
    
    total_ZoomeyeSearch(searchResult)
    说明：从搜索结果中获取搜索到的总数
    参数：hostSearch()的结果或者webSearch（）的结果
    返回值：搜索结果的总数
    
