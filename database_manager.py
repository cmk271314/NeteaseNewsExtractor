import sqlite3
import logging

# 配置 database_manager.py 的日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("database_manager.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class DatabaseManager:
    def __init__(self, db_name):
        """初始化数据库连接"""
        self.db_name = db_name
        self.connection = None
        logger.info(f"初始化{db_name}数据库管理器")

    def connect(self):
        """数据库连接"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            logger.info(f"成功连接到数据库:{self.db_name}")

        except sqlite3.Error as e:
            logger.error(f"数据库{self.db_name}连接失败:{e}")
            return False
        return True

    def create_table(self, create_table_sql):
        """
        :desc:创建表并记录日志
        :param create_table_sql:
        :return:
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
            logger.info(f"创建表成功")
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"创建表失败:{e}")

    def insert_data(self, insert_sql, data):
        """
        插入数据并记录日志
        :param insert_sql:
        :param data:
        :return:
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_sql, data)
            self.connection.commit()
            logger.info(f"数据插入成功:{data}")
        except sqlite3.Error as e:
            logger.error(f"插入数据失败:{e}")

    def close(self):
        """
        关闭数据库连接并记录日志
        :return:
        """
        if self.connection:
            self.connection.close()
            logger.info(f"{self.db_name}连接已关闭")
