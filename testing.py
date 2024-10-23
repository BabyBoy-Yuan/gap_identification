import requests

url = "http://www.sqfgc.com/sqfc/publish/lp/getPermitInfo.do"
params = {
    "permitid": "AF484E363964CCD249531D8AFDE9C5E6",
    "capcode": "994012FAD9C1716DF08505E1D9E08F7A;260"
}
response = requests.get(url=url, params=params)
response.encoding = 'utf-8'
print(response.status_code)
print(response.json())