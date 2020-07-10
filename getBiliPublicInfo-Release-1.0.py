import urllib.request
import json
import re

vuid="18905641"
role_base_url="https://api.bilibili.com/x/space/acc/info"
follow_base_url="https://api.bilibili.com/x/relation/stat" 
view_base_url="https://api.bilibili.com/x/space/upstat"
elec_base_url="ttps://elec.bilibili.com/api/query.rank.do"
referer_base="https://space.bilibili.com/"
all_headers={
    "Host": "api.bilibili.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
}
# 获取基础资料
def get_role(uid):
    referer=referer_base+str(uid)
    all_headers['referer']=referer
    follow_url=role_base_url+'?mid='+str(uid)+'&jsonp=jsonp'    
    follow_req=urllib.request.Request(follow_url,headers=all_headers)
    res=urllib.request.urlopen(follow_req)
    res_tmp = res.read().decode('utf-8')
    print(res_tmp)
    return res_tmp

# 获取粉丝数和关注数
def get_follow(uid):
    referer=referer_base+str(uid)
    all_headers['referer']=referer
    follow_url=follow_base_url+'?vmid='+str(uid)+'&jsonp=jsonp&callback=__jp3'
    follow_req=urllib.request.Request(follow_url,headers=all_headers)
    res=urllib.request.urlopen(follow_req)
    res_tmp = res.read().decode('utf-8')
    print(res_tmp)
    return res_tmp

# 获取播放数和阅读数
def get_view(uid):  
    referer=referer_base+str(uid)
    all_headers['referer']=referer
    view_url=view_base_url+'?mid='+str(uid)+'&jsonp=jsonp&callback=__jp4'
    view_req=urllib.request.Request(view_url,headers=all_headers)
    res=urllib.request.urlopen(view_req)
    res_tmp = res.read().decode('utf-8')
    print(res_tmp)
    return res_tmp

# 获取充电数量
def get_elec(uid):
    referer=referer_base+str(uid)
    all_headers['referer']=referer
    view_url=view_base_url+'?mid='+str(uid)+'&type=jsonp&jsonp=jsonp&callback=__jp8'
    view_req=urllib.request.Request(view_url,headers=all_headers)
    res=urllib.request.urlopen(view_req)
    res_tmp = res.read().decode('utf-8')
    print(res_tmp)
    return res_tmp

# jsonp转json
def loads_jsonp(jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*",jsonp,re.S).group(1))
    except:
        raise ValueError('Invalid Input')

role_json=json.loads(get_role(vuid))
follow_json=loads_jsonp(get_follow(vuid))
view_json=loads_jsonp(get_view(vuid))
elec_json=loads_jsonp(get_elec(vuid))

print("用户uid：",vuid)
print("用户名：",role_json['data']['name'])
print("关注数：",follow_json['data']['following'])
print("粉丝数：",follow_json['data']['follower'])
print("获赞数：",view_json['data']['likes'])
print("播放数：",view_json['data']['archive']['view'])
print("阅读数：",view_json['data']['article']['view'])
try:
    print("充电数：",elec_json['data']['total_count'])
except:
    print("充电数：未开通")