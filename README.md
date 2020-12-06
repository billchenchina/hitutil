# hitutil

`hitutil` 基于 `requests`，是一个与哈尔滨工业大学网络业务相关的支持库。

## ids

统一身份认证相关服务

`ids.idslogin()` 模拟统一身份认证登陆, 返回一个已登陆的 `requests.Session`.

```python3
from hit import ids
session = ids.idslogin('USERNAME', 'PASSWORD')
session.get('http://jwes.hit.edu.cn/queryWsyyIndex') # 登陆本科生网上服务系统
response = session.get('http://jwes.hit.edu.cn/cjcx/queryQmcj') # 查询成绩
```
