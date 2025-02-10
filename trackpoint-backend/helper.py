from redis import Redis


class HBF:
    """h-bloom-filter"""

    def __init__(self, redis: Redis, key: str) -> None:
        self.key = key
        # 布隆过滤器
        self.bloom = redis.bf()
        # 如果不存在再创建，否则会报错
        if not redis.exists(self.key):
            self.bloom.create(self.key, 0.01, 1000)

    def exists(self, fields: str):
        return self.bloom.exists(self.key, fields)

    def mexists(self, *fields: str):
        return self.bloom.mexists(self.key, *fields)

    def add(self, *fields: str):
        if len(fields) == 1:
            return self.bloom.add(self.key, *fields)
        elif len(fields) > 1:
            return self.bloom.madd(self.key, *fields)
