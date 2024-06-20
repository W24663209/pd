import json

from curl_cffi import requests
from lxml import etree


def get_html(result_data):
    return etree.HTML(result_data.text)


cookies = {}
for item in json.loads(open('1.json').read()):
    cookies[item['name']] = item['value']

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    # 'cookie': 'Nop.customer=96fb727a-eeb1-4b78-bf56-2ad14d866d82; _fbp=fb.1.1717245373325.1135332035; __utmz=169439655.1717245374.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); winsourcetech-_zldp=MTBrCk%2FZc3iWWV9uSHk1yJtcEUj0mmkXo82aFrWptHgv5l5w97FuvZypWi6RnJIeb3qDSNrSNME%3D; ASP.NET_SessionId=3bbb04hyw2bh3hwalcxx2ynz; __utmc=169439655; _gcl_au=1.1.924952992.1717664425; __RequestVerificationToken=7-aU_UgCj4pFkKBX-dpXq4DPovjPjy7QLNET6A8Y5XwJbkCeOkQumrCV1SgPM4Mn3BT6fJkPwpEuv1bNNflxJJ-TF-dH2THKdNtxFalh9xg1; __cf_bm=lDoij4sWJOWYiG.FBwcdG.niKXnTZySnhFCUoAvMgyc-1718091661-1.0.1.1-rY9PQvGSHLSi4JbndP6rOX0TSWHjwNpl2I_f.QTVh6KezzDzWUGW8G_MBKGpaOFVM6wD2LQ3JGRcFfm7QzdCNw; __utma=169439655.1464267794.1717245374.1717664425.1718091663.3; __utmt=1; _gid=GA1.2.1729142940.1718091663; trustedsite_visit=1; winsourcetech-_zldt=688612c9-1e2f-40a0-9001-7749fe49ab94-0; NopCommerce.RecentlyViewedProducts=RecentlyViewedProductIds=196463&RecentlyViewedProductIds=165868&RecentlyViewedProductIds=73449; _gat_UA-85980736-1=1; _ga_HRTEXZXY7T=GS1.1.1718091662.2.1.1718091816.0.0.0; __utmb=169439655.10.10.1718091663; _ga_QPHCXYM5J8=GS1.1.1718091663.2.1.1718091816.50.0.0; _ga_7H8JK6K9VW=GS1.1.1718091663.2.1.1718091816.38.0.0; _ga=GA1.2.1740422807.1717664425',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

params = {
    'pagenumber': '1',
}

# 设置代理
# 设置代理用户名和密码
proxy_username = '3965247-c3a28a78'
proxy_password = '17336315-global-25597612'
# 3965247-c3a28a78:17336315-global-25597612@gate-hk.kookeey.info:1000
proxies = {
    'http': f'http://pr.oxylabs.io:7777',
    'https': f'http://pr.oxylabs.io:7777',
}

for i in range(42497):
    response = requests.get('https://www.win-source.net/product/all?pagenumber=%s' % i, impersonate="chrome100",
                            params=params,
                            cookies=cookies, headers=headers)
    # print(response.text)
    # print(response.status_code)

    for url in get_html(response).xpath('//div[@class="picture"]/a/@href'):
        try:
            result = requests.get('https://www.win-source.net' + url, impersonate="chrome100", params=params,
                                  proxies=proxies)
            print('https://www.win-source.net' + url)
            # result = requests.get('https://www.win-source.net/products/detail/texas-instruments/lm324d.html',
            #                       impersonate="chrome100", params=params, cookies=cookies, headers=headers)
            html = get_html(result)
            item = {}
            item['零件编号'] = html.xpath('//tr[@class="product-part-number"]/td[2]')[0].text
            item['制造商'] = html.xpath('//tr[@class="manufacturers"]/td[2]//span/a')[0].text
            item['目录'] = html.xpath('//tr[@class="product-category"]/td[2]')[0].text
            item['描述'] = html.xpath('//tr[@class="short-description"]/td[2]')[0].text
            item['样本'] = html.xpath('//table[@class="productUpperTable"]/tr[4]/td[2]')[0].text
            try:
                item['ECAD 模块'] = html.xpath('//table[@class="productUpperTable"]//tr[6]//a/img/@src')[0]
            except:
                pass
            item['仓库'] = html.xpath(
                '//table[@class="shippingInfoTable"]//tr[@class="product-warehouse"]/td[@class="overview-box-value"]')[
                0].text
            price_units = []
            for ele in html.xpath("//div[contains(@class,'prices-table')]/div[contains(@class,'prices-row')]")[1:]:
                price_unit = {}
                price_unit['数量'] = ele.xpath('div')[0].text.replace('\n', '')
                price_unit['单价'] = ele.xpath('div')[1].text.replace('\n', '')
                price_unit['外部价格'] = ele.xpath('div')[2].text.replace('\n', '')
                price_units.append(price_unit)
            item['price_units'] = price_units
            products_specificationss = []
            for ele in html.xpath('//table[@class="data-table"]/tbody/tr')[1:]:
                products_specifications = {}
                products_specifications[ele.xpath('td')[0].text.replace('\n', '')] = ele.xpath('td')[1].text.replace(
                    '\n',
                    '')
                # print(ele.xpath('td')[0].text,ele.xpath('td')[1].text)
                products_specificationss.append(products_specifications)
            item['products_specificationss'] = products_specificationss
            item['descriptions'] = html.xpath('//div[@class="full-description"]')[0].text
            print(item)
            with open('winsource.json', 'a') as f:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        except:
            pass
