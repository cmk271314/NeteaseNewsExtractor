print(f'脚本开始执行:==========================================')
import os
print(f'当前工作目录: {os.getcwd()}')
import logging.config
import requests
import random
from bs4 import BeautifulSoup
from parse_html import parse_html_file
from database_manager import DatabaseManager
# 配置 control.py 的日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("control.log", encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info("This is a log message from control.py")




urls = []
href='https://news.163.com/world/'
# 调用parse_html里面的parse_html_file函数解析html文件
urls = parse_html_file(href)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}
logger.info(f"正在发起get请求:将进行for循环")
for url in urls:
    # get请求
    logger.info(f"正在发起get请求:{url}")
    responses = requests.get(url, headers=headers)

    if responses.status_code == 200:
        # bs4解析html
        soup = BeautifulSoup(responses.text, "html.parser")
        # 获取标题
        title = soup.find("h1").get_text()

        # 获取作者

        author_div=soup.find('div', class_='creative_statement')or BeautifulSoup('none','html.parser')
        author = author_div.text

        # 提取文章内容
        content = ""
        for p in soup.find("div", class_="post_body").find_all("p"):

            if p.find("b"):
                break
            content += p.text + f"\n"
        data=[random.randint(0,2147483640),author,title,content]
        # 创建表
        try:
            db = DatabaseManager('blog.db')

            if db.connect():
                create_table_sql = """
            CREATE TABLE IF NOT EXISTS blog_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                editor TEXT NOT NULL,
                title TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                remark TEXT)
                """
                db.create_table(create_table_sql)
                db.close()
        except:
            logger.error(f'创建表失败')

        try:
            db = DatabaseManager('blog.db')
            if db.connect():
                insert_sql="""
                INSERT INTO
  blog_posts (user_id, editor, title, content)
VALUES
  (?, ?, ?, ?)
                """
                db.insert_data(insert_sql,data)
                db.close()
            else:
                print(f'插入失败')
        except:
            print(f'插入失败')


    else:
        logger.exception(f"请求{url}异常")


