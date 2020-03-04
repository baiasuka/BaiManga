import redis
import pickle
import config


class RedisConnection:
    """
    直接将查询结果对象序列化存储
    """
    def __init__(self, host=None, port=None, db=None, password=None,ex=None):
        # 创建对本机数据库的连接对象
        if config:
            self.host = host if host else config.REDIS_CACHE_CONFIG['host']
            self.port = port if port else config.REDIS_CACHE_CONFIG['port']
            self.db = db if db else config.REDIS_CACHE_CONFIG['db']
            # self.expires = ex or config.REDIS_CACHE_CONFIG['expired']
            self.password = password if password else config.REDIS_CACHE_CONFIG['password']
            self.conn = redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password)

    # 存储
    def set(self, key_, value_, ex_=None):
        # 将数据pickle.dumps，转化为二进制bytes数据
        # ex_单位为秒
        value_ = pickle.dumps(value_)
        # 将数据存储到数据库
        if ex_:
            self.conn.set(key_, value_, ex=ex_)
        else:
            self.conn.set(key_, value_)
        return True

    # 读取
    def get(self, key_):
        # 从数据库根据键（key）获取值
        value_ = self.conn.get(key_)
        if value_:
            value_ = pickle.loads(value_)  # 加载bytes数据，还原为python对象
            return value_
        else:
            # 为None(值不存在)，返回空列表
            return None

    # 删除
    def delete(self, key_):
        self.conn.delete(key_)
        return 'deleted'

    def get_conn(self):
        """
        获取Redis数据库连接对象
        :return:
        """
        return self.conn

if __name__ == '__main__':
    redis = RedisConnection()
    redis.set("test_list", ["hong", "hou"])
    r = redis.get("test_list")
    print(r)
