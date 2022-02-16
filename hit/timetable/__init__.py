import requests
import json
import pandas as pd


def query_by_gxh(gxh: str, semester: str, weekday: int, s: requests.sessions.Session=None):
    if s is None:
        s = requests.Session()
    r = s.post(url='https://wxfwdt.hit.edu.cn/app/bkskbcx/kbcxapp/getBkszkb', data={
        'info': json.dumps({
            'gxh': gxh,
            'zc': str(weekday),
            'xnxq': semester,
        })
    })
    return r.json()['module']['data']


def parse_to_df(result):
    res = pd.DataFrame(result)
    col = ['上课地点', '教师', '课程名', '周次', '_', '上课时间', '星期', '__']
    try:
        res.columns = col
    except ValueError:
        res = pd.DataFrame(columns=col)
    res.drop(columns='_', inplace=True)
    res.drop(columns='__', inplace=True)
    return res
