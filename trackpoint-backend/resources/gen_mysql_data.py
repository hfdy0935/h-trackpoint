# import random
# import json
# from datetime import datetime, timedelta
# from re import A

# import numpy as np


# def generate_page_url():
#     """生成随机页面url"""
#     return random.choice([
#         "http://www.example.com/shopping",
#         "http://www.example.com/cart",
#         "http://www.example.com/checkout",
#         "http://www.example.com/product/123",
#         "http://www.example.com/product/456",
#         "http://www.example.com/product/789",
#         "http://www.example.com/user/profile",
#         "http://www.example.com/user/orders",
#         "http://www.example.com/user/wishlist",
#         "http://www.example.com/user/settings"
#     ])


# def generate_client_id():
#     return random.choice([str(i) for i in range(501)])


# def generate_time():
#     # 定义权重：白天（8-18点）概率高，其他时间概率低
#     hour = random.choices(
#         range(0, 24),
#         weights=[1] * 8 + [5] * 10 + [1] * 6,
#         k=1
#     )[0]
#     minute = random.randint(0, 59)
#     second = random.randint(0, 59)
#     # 定义权重：工作日（周一至周五）概率高，周末概率低
#     day = random.choices(
#         range(1, 29),
#         weights=[5] * 5 + [1] * 2+[5] * 5 + [1] *
#         2+[5] * 5 + [1] * 2+[5] * 5 + [1] * 2,
#         k=1
#     )[0]
#     month = random.randint(1, 12)
#     return datetime(2024, month, day, hour, minute, second).strftime("%Y-%m-%d %H:%M:%S")


# def generate_client():
#     """生成client数据"""
#     # 定义操作系统、浏览器、设备类型的选项
#     os_list = ['Windows', 'macOS', 'Linux', 'Android', 'iOS']
#     os_version_map = {
#         'Windows': ['10', '11'],
#         'macOS': ['12.0', '13.0'],
#         'Linux': ['Ubuntu 20.04', 'Ubuntu 22.04'],
#         'Android': ['11', '12'],
#         'iOS': ['15', '16']
#     }
#     browser_list = ['Chrome', 'Edge', 'Safari', 'Firefox']
#     browser_version_map = {
#         'Chrome': ['131.0.0.0', '132.0.0.0'],
#         'Edge': ['95.0.1020.40', '96.0.1054.29'],
#         'Safari': ['15.0', '16.0'],
#         'Firefox': ['93.0', '94.0']
#     }
#     device_list = ['Desktop', 'Laptop', 'Mobile']

#     # 生成随机经纬度（中国范围内）

#     def random_lng_lat():
#         # 中国经纬度范围
#         lng_min, lng_max = 110, 121
#         lat_min, lat_max = 35, 41
#         lng = round(random.uniform(lng_min, lng_max), 2)
#         lat = round(random.uniform(lat_min, lat_max), 2)
#         return lng, lat

#     records = []
#     for i in range(400, 500):
#         id = str(i)
#         os = random.choice(os_list)
#         os_version = random.choice(os_version_map[os])
#         browser = random.choice(browser_list)
#         browser_version = random.choice(browser_version_map[browser])
#         device = random.choice(device_list)
#         lng, lat = random_lng_lat()

#         record = (
#             id, os, os_version, browser, browser_version, device, lng, lat
#         )
#         records.append(record)

#     sql_template = "INSERT INTO `trackpoint`.`client` (`id`, `os`, `os_version`, `browser`, `browser_version`, `device`, `lng`, `lat`) VALUES\n"
#     values = []
#     for record in records:
#         values.append(
#             f"('{record[0]}', '{record[1]}', '{record[2]}', '{record[3]}', '{record[4]}', '{record[5]}', {record[6]}, {record[7]})")

#     sql = sql_template + ",\n".join(values) + ";"
#     with open('./mysql-data/client.sql', 'a') as f:
#         f.write(sql)


# def generate_default_event_error_record():
#     """生成报错事件上报记录"""
#     import random
#     from datetime import datetime, timedelta

#     # 固定值
#     project_id = '4d465457-2804-4abe-9783-4f3f032c212a'
#     event_id = '4'
#     screen_shot_path = ''

#     # 随机报错原因列表
#     error_reasons = [
#         "资源观察错误",
#         "内存/堆栈错误",
#         "类型错误",
#         "网络错误",
#         "JSON 解析错误",
#         "资源加载错误",
#         "引用错误",
#         "语法错误",
#         "DOM 操作错误",
#         "未知脚本错误"
#     ]

#     # 生成 500 条记录
#     records = []
#     for i in range(1, 2001):
#         id = str(i)
#         client_id = generate_client_id()
#         create_time = generate_time()
#         params = json.dumps(
#             {"error_reason": random.choice(error_reasons)}).replace('"', '\\"')

#         record = (
#             id, project_id, event_id, client_id, create_time, generate_page_url(
#             ), screen_shot_path, params
#         )
#         records.append(record)

#     # 打印生成的 SQL 语句
#     sql_template = "INSERT INTO `trackpoint`.`record` (`id`, `project_id`, `event_id`, `client_id`, `create_time`, `page_url`, `screen_shot_path`, `params`) VALUES\n"
#     values = []
#     for record in records:
#         values.append(
#             f"('{record[0]}', '{record[1]}', '{record[2]}', '{record[3]}', '{record[4]}', '{record[5]}', '{record[6]}', '{record[7]}')")

#     sql = sql_template + ",\n".join(values) + ";"
#     with open('./mysql-data/default_error.sql', 'a', encoding='utf-8') as f:
#         f.write(sql)


# def generate_default_event_request_record():
#     """请求记录"""
#     import random
#     from datetime import datetime, timedelta
#     import json

#     # 定义固定参数
#     project_id = '4d465457-2804-4abe-9783-4f3f032c212a'
#     event_id = '5'

#     def randoM_method():
#         methods = ['GET']*10+['POST']*8+['PUT']*5+['DELETE'] * \
#             3+['PATCH']*2+['HEAD']*1+['OPTIONS']*1+['TRACE']
#         return random.choice(methods)

#     # 生成SQL语句
#     values = []
#     for i in range(2001, 5001):
#         client_id = str(random.randint(1, 199))
#         create_time = generate_time()
#         status_code = random.choice([200]*7+[404]*3+[403]*2+[500]*2+[422]*2+[
#                                     502]*1+[503]*1+[504]*1)  # 包括你指定的四个状态码和其他常见状态码
#         time_duration = round(random.uniform(0.01, 5.0), 2)
#         request_method = randoM_method()
#         request_url = generate_page_url()
#         params = r'{\"request_url\":\"'+request_url+r'\",\"status_code\":'+str(
#             status_code)+r',\"time_duration\":'+str(time_duration)+r',\"request_method\":\"'+request_method+r'\"}'

#         values.append(
#             f"('{i}', '{project_id}', '{event_id}', '{client_id}', '{create_time}', '{request_url}', '', '{params}')")

#     with open('./mysql-data/default_request.sql', 'a') as f:
#         f.write(f"INSERT INTO `trackpoint`.`record` (`id`, `project_id`, `event_id`, `client_id`, `create_time`, `page_url`, `screen_shot_path`, `params`) VALUES\n" + ",\n".join(values) + ";")


# def generate_custom_event_click_record():
#     """生成自定义点击按钮事件的记录"""
#     import random
#     from datetime import datetime, timedelta
#     import json

#     # 定义固定参数
#     project_id = '4d465457-2804-4abe-9783-4f3f032c212a'
#     event_id = 'fb4e2a4b-2088-421e-9651-75051e5becf5'
#     # 生成SQL语句
#     sql_values = []
#     for i in range(5001, 6001):
#         id = str(i)
#         client_id = generate_client_id()
#         create_time = generate_time()
#         page_url = generate_page_url()

#         # 随机生成params
#         params = {
#             "id": str(i),
#             "name": "固定商品名称",  # 固定名称
#             "time": create_time,  # 随机时间
#             "type": random.choice(["A", "B", "C", "D"]),  # 随机类型
#             # 随机数组
#             "array": [random.randint(1, 100) for _ in range(random.randint(1, 5))],
#             # 随机对象
#             "object": {f"key{random.randint(1, 10)}": random.randint(1, 100) for _ in range(random.randint(1, 3))},
#             "hasLogin": random.choice([True, False])  # 随机布尔值
#         }
#         params1 = json.dumps(params).replace('"', r'\"')

#         # 构造单条插入值
#         sql_values.append(
#             f"('{id}', '{project_id}', '{event_id}', '{client_id}', '{create_time}', '{page_url}', '', '{params1}')")

#     # 合并所有插入值
#     sql = f"INSERT INTO `trackpoint`.`record` (`id`, `project_id`, `event_id`, `client_id`, `create_time`, `page_url`, `screen_shot_path`, `params`) VALUES\n" + \
#         ",\n".join(sql_values) + ";"
#     with open('./mysql-data/custom_click.sql', 'a', encoding='utf-8') as f:
#         f.write(sql)


# def generate_default_event_performance_record():
#     """生成页面性能记录"""
#     import random
#     from datetime import datetime
#     import json

#     # 定义固定参数
#     project_id = '4d465457-2804-4abe-9783-4f3f032c212a'
#     event_id = '3'
#     dns = [round(i, 2) for i in np.arange(0, 40, 0.01)]
#     tcp = [round(i, 2) for i in np.arange(0, 30, 0.01)]
#     request = [round(i, 2) for i in np.arange(20, 120, 0.01)]
#     response = [round(i, 2) for i in np.arange(30, 200, 0.01)]
#     processing = [round(i, 2) for i in np.arange(60, 600, 0.01)]
#     load_event_duration = [round(i, 2) for i in np.arange(40, 280, 0.01)]
#     js_heap_size_used_percent = [round(i, 2) for i in np.arange(10, 100, 0.01)]

#     # 生成SQL语句
#     sql_values = []
#     for i in range(6001, 9001):
#         id = str(i)

#         # client_id 是1-199的随机字符串
#         client_id = generate_client_id()

#         # 随机生成时间
#         create_time = generate_time()

#         # 随机生成页面性能指标
#         params = {
#             'dns': random.choice(dns),
#             'tcp': random.choice(tcp),
#             'request': random.choice(request),
#             'response': random.choice(response),
#             'processing': random.choice(processing),
#             'load_event_duration': random.choice(load_event_duration),
#             'js_heap_size_used_percent': random.choice(js_heap_size_used_percent),
#         }
#         params1 = json.dumps(params).replace('"', r'\"')

#         # 构造单条插入值
#         sql_values.append(
#             f"('{id}', '{project_id}', '{event_id}', '{client_id}', '{create_time}', '{generate_page_url()}', '', '{params1}')")

#     # 合并所有插入值
#     sql = f"INSERT INTO `trackpoint`.`record` (`id`, `project_id`, `event_id`, `client_id`, `create_time`, `page_url`, `screen_shot_path`, `params`) VALUES\n" + \
#         ",\n".join(sql_values) + ";"
#     with open('./mysql-data/default_performance.sql', 'a') as f:
#         f.write(sql)


# def generate_default_event_click_record():
#     """生成默认点击事件的记录"""
#     import random
#     import json

#     # 固定参数
#     project_id = '4d465457-2804-4abe-9783-4f3f032c212a'
#     event_id = '1'
#     page_url = 'http://www.example.com/cart'
#     screenshot_id = 'resource/29984856bb56d15511e1a0993f82a1e4.png'
#     screen_width, screen_height = 1920, 1080  # 一般电脑屏幕分辨率

#     # 假设商品按钮的热点区域是屏幕中间的一个区域
#     hot_area_x = screen_width // 2
#     hot_area_y = screen_height // 2
#     hot_area_radius = 100  # 热点区域的半径

#     # 生成SQL语句
#     sql_values = []
#     for i in range(9001, 12000):
#         id = str(i)  # id 从1到500的字符串
#         client_id = generate_client_id()

#         # 随机生成点击位置
#         if random.random() < 0.8:  # 80%的概率点击热点区域
#             x = random.randint(hot_area_x - hot_area_radius,
#                                hot_area_x + hot_area_radius)
#             y = random.randint(hot_area_y - hot_area_radius,
#                                hot_area_y + hot_area_radius)
#         else:  # 20%的概率点击其他位置
#             x = random.randint(0, screen_width)
#             y = random.randint(0, screen_height)

#         # 固定的屏幕分辨率
#         w, h = screen_width, screen_height

#         # 构造params
#         params = {
#             "h": h,
#             "w": w,
#             "x": x,
#             "y": y
#         }
#         params1 = json.dumps(params).replace('"', r'\"')
#         create_time = generate_time()

#         # 构造SQL插入语句
#         sql_values.append(
#             f"('{id}', '{project_id}', '{event_id}', '{client_id}','{create_time}', '{page_url}', '{screenshot_id}', '{params1}')"
#         )

#     # 合并所有插入值
#     sql = f"INSERT INTO `trackpoint`.`record` (`id`, `project_id`, `event_id`, `client_id`, `create_time`, `page_url`, `screen_shot_path`, `params`) VALUES\n" + \
#         ",\n".join(sql_values) + ";"
#     with open('./mysql-data/default_click.sql', 'a') as f:
#         f.write(sql)


# def gen_default_event_page_stay_duration():

#     project_id = "4d465457-2804-4abe-9783-4f3f032c212a"
#     event_id = "2"

#     # 生成 SQL 插入语句
#     sql_insert = "INSERT INTO record (id, project_id, event_id, client_id, create_time, page_url, screen_shot_path, params) VALUES\n"

#     # 生成 200 条记录
#     records = []
#     for i in range(12001, 13001):
#         # 生成随机 client_id（UUID 格式）
#         client_id = generate_client_id()

#         create_time = generate_time()

#         # 随机选择页面 URL
#         page_url = generate_page_url()

#         # 随机生成页面停留时间
#         time_duration = random.randint(1, 40)
#         params = json.dumps(
#             {"time_duration": time_duration}).replace('"', r'\"')

#         # 构造记录
#         record_id = str(2501 + i)
#         record = f"('{record_id}', '{project_id}', '{event_id}', '{client_id}', '{create_time}', '{page_url}', '', '{params}')"
#         records.append(record)

#     # 将所有记录拼接为完整的 SQL 语句
#     sql_insert += ",\n".join(records) + ";"
#     with open('./mysql-data/default_page_duration.sql', 'a') as f:
#         f.write(sql_insert)


# if __name__ == '__main__':
    #     generate_client()
    # generate_default_event_error_record()
#     generate_default_event_request_record()
#     generate_custom_event_click_record()
#     generate_default_event_performance_record()
#     generate_default_event_click_record()
#     gen_default_event_page_stay_duration()
