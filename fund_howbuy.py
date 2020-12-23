from lxml import etree
import asyncio
import aiohttp


async def ratio(code):
    conn = aiohttp.TCPConnector(ssl=False)  # 防止ssl报错
    # 实时的估值涨幅
    url_ratio = f'http://www.howbuy.com/fund/ajax/gmfund/valuation/valuationnav.htm?jjdm={code}'
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.request("GET", url=url_ratio) as resp:
            r = await resp.text()
            html = etree.HTML(r)
            expect_growth = html.xpath('//li/span[3]/text()')[0].strip()
            # print(expect_growth)
            ratio_data = {'expectGrowth': expect_growth.replace('%', '')}
            # print(ratio_data)

    # 最近1周，1个月，3个月的增幅
        url_growth = f'http://www.howbuy.com/fund/{code}'
        async with session.request("GET", url=url_growth) as resp:
            # print(response.text)
            r = await resp.text()
            html = etree.HTML(r)
            name = html.xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[1]/div/div[1]/h1/text()')[0]
            value_list = html.xpath('//*[@id="nTab9_0"]/table/tr[2]/td[@class="to-right"]/span/text()')
            last_week_growth, last_month_growth, last_three_months_growth = [i.replace('%', '') for i in value_list][1:4]
            growth_data = {
                'code': code,
                'name': name,
                'lastWeekGrowth': last_week_growth,
                'lastMonthGrowth': last_month_growth,
                'lastThreeMonthsGrowth': last_three_months_growth,
            }
            # print(growth_data)
    # 合并数据
    growth_data.update(ratio_data)
    return growth_data



def stock():
    import requests
    url = "https://data.howbuy.com/cgi/fund/indexmarketdata.json?q=s_sh000001,s_sz399001,s_sh000300,s_sz399006"
    response = requests.get(url)
    r = response.text
    # print(r.split())
    stock_data = []
    for i in r.split():
        tmp = {}
        info = i.split('~')
        tmp['name'], tmp['code'], tmp['price'], tmp['priceChange'], tmp['changePercent'] = info[1:6]
        tmp['date'] = ''
        stock_data.append(tmp)
    return stock_data


def asyncio_(code_list):
    return_data = []
    tasks = []
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    for code in code_list:
        tasks.append(asyncio.ensure_future(ratio(code)))
    loop.run_until_complete(asyncio.wait(tasks))
    for i in tasks:
        return_data.append(i.result())
    loop.close()
    return return_data


if __name__ == '__main__':
    import time
    s_time = time.time()
    code_list = ['005827', '163417']
    data = asyncio_(code_list)
    for i in data:
        print(i)
    for i in stock():
        print(i)
    print('用时：', time.time()-s_time)

