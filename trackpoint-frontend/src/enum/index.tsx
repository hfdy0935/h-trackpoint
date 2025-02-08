import { HomeOutlined, LineChartOutlined, AppstoreOutlined, ApiOutlined, BugOutlined, UserAddOutlined, SelectOutlined, FileSyncOutlined, FundProjectionScreenOutlined, AlertOutlined } from '@ant-design/icons-vue'
import type { VNode } from 'vue';


/**
 * 主页对话框类型
 */
export enum AccountOpEnum {
    LOGIN = '登录',
    REGISTER = '注册',
    UPDATE_PWD = '修改密码'
}



export type SideMenuKey = 'Main' | 'Data' | 'DataStatistic' | 'PerformanceMonitor' | 'MonitorAlert' | 'UserBehaviorAnalysis' | 'Project' | 'Event' | 'Test'
/**
 * 侧边栏菜单项的item
 */
export enum SideMenuEnum {
    Main = '/dashboard/', // 首页
    Data = '/data',// 数据看板
    DataStatistic = '/data-statistic', // 数据统计
    PerformanceMonitor = '/performance-monitor', // 性能监控
    MonitorAlert = '/monitor-alert', // 监控报警
    UserBehaviorAnalysis = '/user-behavior-analysis',// 用户行为分析
    Project = '/project',// 项目管理
    Event = '/event',// 事件关理
    Test = '/test' // 调试
}

/**
 * 侧边栏对应的路由组件名
 */
export const SideMenuNameEnum: Record<SideMenuKey, string> = {
    Main: 'Main', // 首页
    Data: 'Data',
    DataStatistic: 'DataStatistic', // 数据统计
    PerformanceMonitor: 'PerformanceMonitor', // 性能监控
    MonitorAlert: 'MonitorAlert', // 监控报警
    UserBehaviorAnalysis: 'UserBehaviorAnalysis',// 用户行为分析
    Project: 'Project',// 项目管理
    Event: 'Event',// 事件关理
    Test: 'Test' // 调试
}


/**
 * 侧边栏菜单项的icon
 */
export const SideMenuIcon: Record<SideMenuKey, VNode> = {
    Main: <HomeOutlined />, // 首页
    Data: <LineChartOutlined />, // 数据看板
    DataStatistic: <FileSyncOutlined />, // 数据统计
    PerformanceMonitor: <FundProjectionScreenOutlined />, // 性能监控
    MonitorAlert: <AlertOutlined />, // 监控报警
    UserBehaviorAnalysis: <UserAddOutlined />, // 用户行为分析
    Project: <AppstoreOutlined />, // 项目管理
    Event: <ApiOutlined />, // 事件管理
    Test: <BugOutlined /> // 测试
};


/**
 * 项目、事件、用户的状态
 */
export enum StatusEnum {
    NORMAL = 1, // 正常
    DISABLED = 0 // 停用或封禁
}


/**
 * 事件类型枚举
 */
export enum EventTypeEnum {
    /**
     * 默认事件
     */
    DEFAULT = 'default',
    /**
     * 自定义事件
     */
    CUSTOM = 'custom'
}