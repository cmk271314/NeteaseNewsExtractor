import parse_html
import logging


# 配置 control.py 的日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(".venv/partest.log", encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



href='https://news.163.com/world/'

list_hrefs = parse_html.parse_html_file(href)
for href_ in list_hrefs:
    print(f'{href_}\n')
