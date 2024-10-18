import inspect
import logging
import  os
import requests
from bs4 import BeautifulSoup


# 配置 parse_html.py 的日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("parse_html.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# =================================

# 打印当前工作目录和日志文件的绝对路径
print(f"当前工作目录: {os.getcwd()}")
print(f"日志文件路径: {os.path.abspath('parse_html.log')}")
logger.info(f"进入库:{__name__}")

def parse_html_file(url):
    """
    :description:将html文件解析为列表并返回
    :param url:请求地址
    :return:list_hrefs:解析后得到的数据列表
    """

    logger.info(f"进入函数{inspect.currentframe().f_code.co_name}")
    # 请求头设置
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }
    # get请求并解析文件
    logger.info(f"向{url}发起请求")
    try:
        responses = requests.get(url, headers=headers)
        responses.raise_for_status()  # 如果响应状态码不是2xx，将引发HTTPError异常
    except requests.exceptions.HTTPError as http_err:

        logger.exception(f"请求{url}失败:http错误{http_err}")
        return False
    except Exception as e:
        logger.exception(f"其它异常:{e}")
        return False
    else:
        logger.info(f"请求{url}:成功")
        # 空列表list_hrefs用来存放解析出来的href
        list_hrefs = []
        logger.info("开始解析报文html")
        try:
            # 开始解析
            soup = BeautifulSoup(responses.text, "html.parser")
            # 获取url列表
            list_urls = soup.find("div", class_="hidden").find_all("a")
            logger.info(f"解析完成，获得{len(list_urls)}行数据")
        except Exception as parser_err:
            logger.exception(f"解析异常{parser_err}")
            return False
        else:

            for list_url in list_urls:
                list_hrefs.append(list_url.get("href"))
            return list_hrefs




# href='https://news.163.com/world/'
#
# list_hrefs = parse_html_file(href)
# for href_ in list_hrefs:
#     print(f'{href_}\n')
