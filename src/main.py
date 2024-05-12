# 导入
import concurrent.futures
import json
import sys
import threading
import time

from DrissionPage import ChromiumPage, ChromiumOptions
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from utils import ocr
from utils import date_util
from utils import parse_util

path = sys.path[0]


class DownloadHandler(FileSystemEventHandler):

    def on_created(self, event):
        try:
            downloaded_file_path = event.src_path  # type:str
            if downloaded_file_path.endswith('xlsx'):
                thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
                xlsx = parse_util.xlsx(downloaded_file_path)
                # for text in open('src/download/STATEMENT.csv').read().split('\n')[19:-5]:
                #     pass
                thread_pool.shutdown(wait=True)
        except:
            pass


class ChromeCrawl:

    def __init__(self):
        # 设置文件系统监控
        # event_handler = DownloadHandler()
        # observer = Observer()
        # observer.schedule(event_handler, path='%s/download' % path, recursive=False)
        # observer.start()
        # 创建页面对象
        co = ChromiumOptions()
        # co.headless()
        # co.no_imgs()
        self.page = ChromiumPage(co)
        self.download = 'https://yonobusiness.sbi/yono-captcha/gencaptcha'
        # self.download_url = 'https://corp.onlinesbi.sbi/saral/downloadstatement.htm'
        self.page.listen.start([self.download])  # 开始监听，指定获取包含该文本的数据包
        self.captcha = None
        self.captcha_res = None
        threading.Thread(target=self.listen).start()
        self.page.set.download_path('%s/download' % path)  # 设置总路径
        self.start()

    def read_xlsx(self, name):
        thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        parse_util.xlsx('%s/download/%s' % (path,name))
        # for text in open('src/download/STATEMENT.csv').read().split('\n')[19:-5]:
        #     pass
        thread_pool.shutdown(wait=True)

    def listen(self):
        for packet in self.page.listen.steps(timeout=60):
            print(f'拦截\turl:{packet.target}\n内容:{packet.response.body}')
            if packet.target.__eq__(self.download):
                pass
            # elif packet.target.__eq__(self.download_url):
            #     pass

    def input(self, css, value, msg, count=0):
        if count >= 10:
            return
        try:
            print(f'匹配:{css}\t输入:{msg}\t内容:{value}')
            self.page.ele(css).input(value)
        except:
            count += 1
            self.input(css, value, msg, count)

    def click(self, css, msg, count=0):
        try:
            if count >= 10:
                return
            print(f'匹配:{css}\t点击:{msg}')
            self.page.ele(css).click()
        except:
            count += 1
            self.click(css, msg, count)

    def run_js(self, css, msg, count=0):
        print(f'{msg}\t执行js:{css}\t重试次数:{count}')
        try:
            if count >= 10:
                return
            self.page.run_js(css)
        except:
            time.sleep(1)
            count += 1
            self.run_js(css, count)

    def start(self):
        # 访问网页
        self.page.get(
            'https://ibankpro.providusbank.com/IBS/Rl5IW1xkVwNzUTxYQFwIBS2012.do?TF5dRVNYViRTVS0IBS2012=Rl5IW1wb&WkNAUVdZQQIBS2012IBS2012=Xl5EV1wIBS2012')
        self.input('#userName', 'DOMK BOUTIQUE', '账号')
        self.run_js('validateForm()', '下一步')
        self.input('#PASSWORD', 'BallonJay@20568', '密码')
        self.run_js('validateFormLogin2()', '登陆')
        # time.sleep(2)
        self.click('tag:a@@text():1305016781', '账号详情:1305016781')
        # time.sleep(3)
        self.click('tag:input@@value:View Account Statement', '结算详情:View Account Statement')
        # # 在页面中查找元素
        while True:
            # self.input('#datepicker', date_util.mdy(-24 * 60 * 5), '开始时间')
            self.run_js('document.querySelector("#datepicker").value="%s"' % date_util.dmy(-24 * 60 * 5), '开始时间')
            self.run_js('document.querySelector("#traType").value="2"', '代收')
            # self.click('#Filter0', '选择时间')
            # time.sleep(3)
            self.run_js('''
                  this.disabled = true;document.getElementById('IBS').submit();
                  ''', '订单详情')
            self.page.set.download_file_name('订单列表.xlsx')
            self.run_js('''Export_To_File('XLSX')''', '下载')
            self.page.set.when_download_file_exists('overwrite')
            self.page.wait.download_begin()  # 等待下载开始
            self.page.wait.all_downloads_done()  # 等待所有任务结束
            self.read_xlsx('订单列表.xlsx')
            self.click('tag:input@@value:Back', '返回:Back')
            time.sleep(15)


if __name__ == '__main__':
    ChromeCrawl()
