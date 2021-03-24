
import json
import requests
from bs4 import BeautifulSoup

def query_by_rname(s: requests.sessions.Session, rname: str) -> dict:
    s.get('http://ele.hit.edu.cn/')
    suggestions = s.get(
        'http://ele.hit.edu.cn/eleServer/query/rooms.htm', params={'rName': rname})
    rid = json.loads(suggestions.text)['suggestions'][0]['data']
    r = s.get('http://ele.hit.edu.cn/eleServer/query/student.htm', params={
        'rId': rid,
        'rName': rname,
    })
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = soup.findAll('h5')
    values = soup.findAll('h2')
    assert len(tags) == len(values)
    ret = {}
    for i in range(len(tags)):
        ret[tags[i].text] = values[i].text
    return ret
