import requests


def nasdaq():
    """
    爬取sina财经nasdaq基础数据
    :return: 构建的标准返回格式，只包含当日的数据，无历史数据
    """
    url = "http://hq.sinajs.cn/?rn=1609213839262&list=gb_$ndx"
    r = requests.get(url)
    response = r.text
    if r.status_code == 200:
        data = response.split('=')[1].split(',')
        nasdaq_data = {'name': data[0].strip('"'), 'code': '040046', 'price': data[1], 'priceChange': data[4], 'expectGrowth': data[2], 'dayGrowth': data[2], 'lastWeekGrowth': '-', 'lastMonthGrowth': '-', 'lastThreeMonthsGrowth': '-', 'date': ''}
        return nasdaq_data
    else:
        print(f'nasdaq return error: \n {response}')


if __name__ == '__main__':
    nasdaq_data = nasdaq()
    for k, v in nasdaq_data.items():
        print(f'{k}: {v}')
