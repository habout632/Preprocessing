# 引入云API入口模块
# from src.QcloudApi.qcloudapi import QcloudApi

'''
module 设置需要加载的模块
已有的模块列表：
cvm      对应   cvm.api.qcloud.com
cdb      对应   cdb.api.qcloud.com
lb       对应   lb.api.qcloud.com
trade    对应   trade.api.qcloud.com
sec      对应   csec.api.qcloud.com
image    对应   image.api.qcloud.com
monitor  对应   monitor.api.qcloud.com
cdn      对应   cdn.api.qcloud.com
wenzhi   对应   wenzhi.api.qcloud.com
bm       对应   bm.api.qcloud.com
bmlb     对应   bmlb.api.qcloud.com
bmeip    对应   bmeip.api.qcloud.com
bmvpc    对应   bmvpc.api.qcloud.com

'''
from QcloudApi.qcloudapi import QcloudApi

module = 'wenzhi'

'''
action 对应接口的接口名，请参考产品文档上对应接口的接口名
'''
action = 'TextKeywords'

config = {
    'Region': 'sz',
    'secretId': 'AKIDEONH9HCCXjlgUOtrJZ6jAPTM3d6OpXbY',
    'secretKey': '你的secretKey',
    'method': 'get'
}

'''
params 请求参数，请参考产品文档上对应接口的说明
'''
params = {
    'title': '127.0.0.1',
    'content': 0,
    # 'Region': 'gz', # 当Region不是上面配置的DefaultRegion值时，可以重新指定请求的Region
}
try:
    service = QcloudApi(module, config)

    # 请求前可以通过下面四个方法重新设置请求的secretId/secretKey/region/method参数
    # 重新设置请求的secretId
    secretId = '你的secretId'
    service.setSecretId(secretId)
    # 重新设置请求的secretKey
    secretKey = '你的secretKey'
    service.setSecretKey(secretKey)
    # 重新设置请求的region
    region = 'sz'
    service.setRegion(region)
    # 重新设置请求的method
    method = 'post'
    service.setRequestMethod(method)

    # 生成请求的URL，不发起请求
    print(service.generateUrl(action, params))
    # 调用接口，发起请求
    print(service.call(action, params))
except Exception as e:
    print('exception:', e)
