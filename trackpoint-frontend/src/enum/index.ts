import {
  HomeOutlined,
  LineChartOutlined,
  AppstoreOutlined,
  ApiOutlined,
  BugOutlined,
  UserAddOutlined,
  FileSyncOutlined,
  FundProjectionScreenOutlined,
  SendOutlined,
} from '@ant-design/icons-vue'
import { h, type VNode } from 'vue'

/**
 * 主页对话框类型
 */
export enum AccountOpEnum {
  LOGIN = '登录',
  REGISTER = '注册',
  UPDATE_PWD = '修改密码',
}

export type SideMenuKey =
  | 'Main'
  | 'Data'
  | 'ProjectOverview'
  | 'PerformanceMonitor'
  | 'UserAnalysis'
  | 'Project'
  | 'Event'
  | 'Record'
  | 'Test'
/**
 * 侧边栏菜单项的item
 */
export enum SideMenuPathEnum {
  Main = '/dashboard/', // 首页
  Data = '/data', // 数据看板
  ProjectOverview = '/project-overview', // 项目总览
  PerformanceMonitor = '/performance-monitor', // 性能监控
  UserAnalysis = '/user-analysis', // 用户分析
  Project = '/project', // 项目管理
  Event = '/event', // 事件管理
  Record = '/record', // 上报事件管理
  Test = '/test', // 调试
}

/**
 * 侧边栏对应的路由组件名
 */
export const SideMenuNameEnum: Record<SideMenuKey, string> = {
  Main: 'Main', // 首页
  Data: 'Data',
  ProjectOverview: 'ProjectOverview', // 项目总览
  PerformanceMonitor: 'PerformanceMonitor', // 性能监控
  UserAnalysis: 'UserAnalysis', // 用户分析
  Project: 'Project', // 项目管理
  Event: 'Event', // 事件管理
  Record: 'Record', // 上报事件管理
  Test: 'Test', // 调试
}

/**
 * 侧边栏菜单项的icon
 */
export const SideMenuIcon: Record<SideMenuKey, VNode> = {
  Main: h(HomeOutlined), // 首页
  Data: h(LineChartOutlined), // 数据看板
  ProjectOverview: h(FileSyncOutlined), // 项目总览
  PerformanceMonitor: h(FundProjectionScreenOutlined), // 性能监控
  UserAnalysis: h(UserAddOutlined), // 用户分析
  Project: h(AppstoreOutlined), // 项目管理
  Event: h(ApiOutlined), // 事件管理
  Record: h(SendOutlined), // 上报事件管理
  Test: h(BugOutlined), // 测试
}

/**
 * 项目、事件、用户的状态
 */
export enum StatusEnum {
  NORMAL = 1, // 正常
  DISABLED = 0, // 停用或封禁
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
  CUSTOM = 'custom',
}
