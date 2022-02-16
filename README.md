# hitutil

`hitutil` 基于 `requests`，是一个与哈尔滨工业大学网络业务相关的支持库。

## ids

统一身份认证相关服务

`ids.idslogin()` 模拟统一身份认证登陆, 返回一个已登陆的 `requests.Session`.

```python
from hit import ids
session = ids.idslogin('USERNAME', 'PASSWORD')
session.get('http://jwes.hit.edu.cn/queryWsyyIndex') # 登陆本科生网上服务系统
response = session.get('http://jwes.hit.edu.cn/cjcx/queryQmcj') # 查询成绩
```


## timetable

课表相关服务

```python
from hit import timetable

def main():
    print(timetable.parse_to_df(timetable.query_by_gxh('学号', '学期', '''周次，整数'''))) # 学期类似：'2021-2022;1' 表示秋季学期

if __name__ == '__main__':
    main()
```

### 学期参数说明

| 接口参数 | 对应实际学期 |
| ----------- | ------------ |
| 2020-2021;1 | 2020秋季   |
| 2020-2021;2 | 2021春季   |
| 2020-2021;3 | 2021夏季   |
| 2020-2021;4 | 2021暑假   |
| 2020-2021;5 | 2021寒假   |
| 2021-2022;1 | 2021秋季   |
| ...          | ...          |