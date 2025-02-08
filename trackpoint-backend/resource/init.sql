/*!40101 SET NAMES utf8 */;
# 告诉docker初始化时用utf-8，避免中文乱码
DROP DATABASE IF EXISTS trackpoint;

create database trackpoint DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;

use trackpoint;

DROP TABLE IF EXISTS user;

create TABLE user (
    id VARCHAR(36) NOT NULL COMMENT '用户id',
    email varchar(30) comment '邮箱，可选，可以用github登录',
    nickname VARCHAR(20) DEFAULT '' COMMENT '用户昵称',
    password VARCHAR(32) NOT NULL COMMENT '用户密码md5结果',
    create_time datetime NOT NULL COMMENT '注册时间',
    update_time datetime not null comment '修改时间',
    status tinyint unsigned not null default 1 comment '状态，1正常0封禁',
    is_admin TINYINT unsigned NOT NULL DEFAULT 0 COMMENT '是否是管理员，0不是1是',
    project_num_limit TINYINT unsigned NOT NULL COMMENT '用户项目数量限制',
    event_num_limit TINYINT unsigned NOT NULL COMMENT '用户单个项目的上报接口限制',
    PRIMARY KEY (id)
) COMMENT = '用户表';

# 邮箱 email@qq.com
# 密码 aaa1234
# 普通用户
INSERT INTO `user` (`id`, `email`, `nickname`, `password`, `create_time`, `update_time`, `status`, `is_admin`, `project_num_limit`, `event_num_limit`) VALUES ('2f459756-9550-4824-a879-a06ed6eb7227', 'email@qq.com', '我是管理员', '1ff97cd8bee5ccd3effdcd146cbff63b', '2025-01-24 22:02:03', '2025-01-24 22:11:09', 1, 0, 10, 200);

create table project (
    id varchar(36) not null comment '项目id',
    name varchar(20) not null comment '项目名',
    description varchar(300) comment '项目描述',
    user_id varchar(36) not null comment '所属用户id',
    `key` varchar(36) not null comment '项目的key',
    create_time datetime NOT NULL COMMENT '创建时间',
    update_time datetime not null comment '修改时间',
    status tinyint unsigned not null default 0 comment '状态，1正常，0下架',
    primary key (id),
    index idx_user_id (user_id)
) comment = '项目表';

CREATE TABLE bind_param (
    id varchar(36) not null comment 'id',
    name varchar(50) not null comment '参数名',
    description varchar(300) comment '参数描述',
    type VARCHAR(10) not null comment '参数类型列表，暂时只支持number、string、boolean、array、object，list、dict里面的参数类型不做进一步限制',
    primary key (id)
) COMMENT '绑定参数表，用于约束上传参数，可自定义';

-- 插入默认事件绑定的参数
-- performance部分参考 https://juejin.cn/post/6844904182202253325
INSERT INTO
    bind_param (id, name, description, type)
VALUES ('1', 'x', '点击的x坐标', 'number'),
    ('2', 'y', '点击的y坐标', 'number'),
    ('3', 'w', '浏览器宽度', 'number'),
    ('4', 'h', '浏览器高度', 'number'),
    (
        '5',
        'error_reason',
        'js报错原因',
        'string'
    ),
    (
        '6',
        'status_code',
        '请求状态码',
        'number'
    ),
    (
        '7',
        'request_method',
        '请求方法',
        'string'
    ),
    (
        '8',
        'request_url',
        '请求url',
        'string'
    ),
    (
        '9',
        'time_duration',
        '一个时间段，页面停留or网络请求，单位ms，保留两位小数',
        'number'
    ),
    (
        '10',
        'dns',
        'DNS查询耗时，单位ms',
        'number'
    ),
    (
        '11',
        'tcp',
        'TCP连接耗时，单位ms',
        'number'
    ),
    (
        '12',
        'request',
        '开始请求到接收到第一个字节的耗时，单位ms',
        'number'
    ),
    (
        '13',
        'response',
        '从接收到第一个至接收到最后一个字节的耗时，单位ms',
        'number'
    ),
    (
        '14',
        'processing',
        '渲染页面耗时，单位ms',
        'number'
    ),
    (
        '15',
        'load_event_duration',
        '资源加载完毕之后，加载事件的耗时，单位ms',
        'number'
    ),
    (
        '16',
        'js_heap_size_used_percent',
        'JS堆占用百分比',
        'number'
    );

-- 默认事件不允许修改
create table default_event (
    id varchar(36) not null comment '事件id',
    name varchar(30) not null comment '事件名',
    description VARCHAR(300) COMMENT '事件描述',
    need_shot TINYINT unsigned NOT NULL DEFAULT 0 COMMENT '事件触发时是否需要截图，0不需要1需要',
    status tinyint unsigned not null default 0 comment '状态，1正常，0下架',
    primary key (id)
) comment '默认事件表';

create table custom_event (
    id varchar(36) not null comment '事件id',
    `name` varchar(30) not null comment '事件名',
    `description` VARCHAR(300) COMMENT '事件描述',
    user_id varchar(36) not null comment '所属用户id',
    create_time datetime NOT NULL COMMENT '创建时间',
    update_time datetime not null comment '修改时间',
    `status` tinyint unsigned not null default 0 comment '状态，1正常，0下架',
    primary key (id),
    index idx_name (name),
    index idx_user_id (user_id)
) COMMENT = '自定义事件';

create table event_project (
    id varchar(36) not null comment 'id',
    event_id varchar(36) not null comment '用户事件id',
    project_id varchar(36) not null comment '项目id',
    primary key (id),
    index idx_custom_event_id (event_id),
    index idx_project_id (project_id)
) COMMENT '用户事件和项目关联表';

CREATE table event_bind_param (
    id varchar(36) not null comment 'id',
    event_id varchar(36) not null comment '事件id',
    bind_param_id varchar(36) not null comment '绑定参数id',
    primary key (id),
    index idx_event_id (event_id),
    index idx_bind_param_id (bind_param_id)
) COMMENT '事件绑定参数关联表';

-- 基本事件
INSERT INTO
    default_event (
        id,
        name,
        description,
        need_shot,
        status
    )
VALUES ('1', 'click', '点击', 1, 1),
    (
        '2',
        'page_stay_duration',
        '页面停留时间',
        0,
        1
    ),
    (
        '3',
        'performance',
        'performance API的部分指标',
        0,
        1
    ),
    ('4', 'js_error', 'JS错误', 0, 1),
    ('5', 'request', '网络请求', 0, 1);

insert into
    event_bind_param
values ('1', '1', '1'), -- 点击的x
    ('2', '1', '2'), -- 点击的y
    ('3', '1', '3'), -- 点击时的浏览器宽度
    ('4', '1', '4'), -- 点击时的浏览器高度
    ('5', '2', '9'), -- 页面停留时间
    ('6', '3', '10'), -- performance DNS查询耗时，单位ms
    ('7', '3', '11'), -- performance TCP连接耗时，单位ms
    ('8', '3', '12'), -- performance 开始请求到接收到第一个字节的耗时，单位ms
    ('9', '3', '13'), -- performance 从接收到第一个至接收到最后一个字节的耗时，单位ms
    ('10', '3', '14'), -- performance 渲染页面耗时，单位ms
    ('11', '3', '15'), -- performance 资源加载完毕之后，加载事件的耗时，单位ms
    ('12', '3', '16'), -- performance JS堆占用百分比
    ('13', '4', '5'), -- js报错原因
    ('14', '5', '6'), -- 请求状态码
    ('15', '5', '7'), -- 请求方法
    ('16', '5', '8'), -- 请求url
    ('17', '5', '9');
-- 请求消耗时间
CREATE TABLE client (
    id varchar(36) COMMENT '客户端uid，由前端生成，注册时为每个客户端生成一个',
    os varchar(20) NULL COMMENT '操作系统',
    os_version varchar(20) NULL COMMENT '操作系统版本',
    browser varchar(20) NULL COMMENT '浏览器',
    browser_version varchar(20) NULL COMMENT '浏览器版本',
    device varchar(20) NULL COMMENT '设备类型',
    lng FLOAT NOT NULL DEFAULT 361 COMMENT '经度',
    lat FLOAT NOT NULL DEFAULT 361 COMMENT '纬度',
    PRIMARY KEY (id)
) COMMENT = '客户端表';

CREATE Table record (
    id varchar(36) not null comment '记录id',
    project_id varchar(36) not null comment '所属项目id',
    event_id varchar(36) not null comment '用户事件id',
    client_id varchar(36) not null comment '设备id',
    create_time datetime NOT NULL COMMENT '创建时间',
    page_url VARCHAR(100) NOT NULL COMMENT '页面url',
    screen_shot_path varchar(100) not null comment '截图储存路径，如有',
    params JSON comment '参数',
    primary key (id),
    index idx_event_id (event_id),
    index idx_client_id (client_id)
) COMMENT = '上报记录表';