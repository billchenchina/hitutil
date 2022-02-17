# 提供jwes成绩查询相关的服务，返回结构化的pandas数据。
import requests
import pandas as pd
from bs4 import BeautifulSoup


def query(s: requests.sessions.Session, xnxq: str = None, sfjg: bool = None, kcmc: str = None, bkcxbj: str = None, pageSize: int = 200):
    """这个函数为你爬取结构化的成绩数据

    Args:
        s (requests.sessions.Session): 已经ids登陆认证的Session
        xnxq (str, optional): 学年学期，默认值为None，表示全部
        sfjg (bool, optional): 是否及格，默认值为None，表示全部
        kcmc (str, optional): 课程名称，默认值为None，表示全部
        bkcxbj (str, optional): 补考重修标记，默认值为None，表示全部
        pageSize (int, optional): 一个比较大的数，让jwes只分一页（避免多次请求）
    """
    s.get('http://jwes.hit.edu.cn/queryWsyyIndex')  # 登陆本科生网上服务系统

    # 构造数据（data）
    data = {}
    data['pageXnxq'] = xnxq if xnxq else ''
    if sfjg is not None:
        data['pageSfjg'] = '是' if sfjg else '否'
    else:
        data['pageSfjg'] = ''
    data['pageKcmc'] = kcmc if kcmc else ''
    data['pageSize'] = str(pageSize)
    data['pageNo'] = '1'
    data['pageBkcxbj'] = bkcxbj if bkcxbj else ''
    data['pageCount'] = '1'

    # 到jwes查询
    r = s.post('http://jwes.hit.edu.cn/cjcx/queryQmcj', data=data)

    # 解析html，定位到成绩数据
    soup = BeautifulSoup(r.text, 'html.parser')
    x = soup.find('table', class_='bot_line')

    # 结构化为pd
    ret = pd.read_html(str(x))[0]
    return ret
