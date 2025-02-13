<template>
    <section>
        <a-row :gutter="[16, 16]" class="statistics-row">
            <!-- 第一列：两个小卡片 -->
            <a-col :span="8">
                <a-row :gutter="[0, 16]">
                    <!-- 今日访客量 -->
                    <a-col :span="24">
                        <a-card class="stat-card">
                            <a-statistic title="今日访客量" :value="todayVisits">
                                <template #suffix>
                                    <EyeOutlined />
                                </template>
                            </a-statistic>
                        </a-card>
                    </a-col>
                    <!-- 今日访问人数 -->
                    <a-col :span="24">
                        <a-card class="stat-card">
                            <a-statistic title="今日访问人数" :value="todayVisitors">
                                <template #suffix>
                                    <TeamOutlined />
                                </template>
                            </a-statistic>
                        </a-card>
                    </a-col>
                </a-row>
            </a-col>

            <!-- 第二列：两个小卡片 -->
            <a-col :span="8">
                <a-row :gutter="[0, 16]">
                    <!-- 今日新增人数 -->
                    <a-col :span="24">
                        <a-card class="stat-card">
                            <a-statistic title="今日新增人数" :value="todayNewUsers">
                                <template #suffix>
                                    <UserAddOutlined />
                                </template>
                            </a-statistic>
                        </a-card>
                    </a-col>
                    <!-- 今日人均访问数 -->
                    <a-col :span="24">
                        <a-card class="stat-card">
                            <a-statistic title="今日人均访问数" :value="avgVisitsPerUser" :precision="2">
                                <template #suffix>
                                    <BarChartOutlined />
                                </template>
                            </a-statistic>
                        </a-card>
                    </a-col>
                </a-row>
            </a-col>

            <!-- 中国地图 -->
            <a-col :span="8">
                <a-card class="map-card">
                    <div ref="chinaMapRef" class="china-map"></div>
                </a-card>
            </a-col>
        </a-row>

        <a-row>
            <a-col :span="24">
                <project-plot />
            </a-col>
        </a-row>
    </section>
</template>

<script setup lang="ts">
import { SideMenuNameEnum } from '@/enum';
import { useUserStore } from '@/store';
import { ApiOutlined, AppstoreOutlined, UserOutlined, EyeOutlined, TeamOutlined, UserAddOutlined, BarChartOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { storeToRefs } from 'pinia';
import { computed, h, watchEffect, type VNode } from 'vue';
import { onMounted, ref } from 'vue';
import ProjectPlot from './project-plot.vue';
import type { RespBaseStat } from '@/type/data/stat/base';
import { reqBaseStat } from '@/api/v1/data';
import * as echarts from 'echarts';
import { registerMap } from 'echarts';


defineOptions({
    name: SideMenuNameEnum.DataStatistic
})

const { user } = storeToRefs(useUserStore())
// 基本信息统计
const data = ref<RespBaseStat>({} as RespBaseStat)
// 顶部激活的类型
type ActiveType = 'project' | 'event' | 'client'
const activeType = ref<ActiveType>('project')
interface ITopDataItem {
    tp: ActiveType
    title: string
    value: number
    icon: VNode
}
/**
 * 顶部显示的数据
 */
const topData = computed<ITopDataItem[]>(() => [
    {
        tp: 'project',
        title: '项目数量',
        value: user.value.projectNum,
        icon: h(AppstoreOutlined)
    },
    {
        tp: 'event',
        title: '事件数量',
        value: user.value.eventNum,
        icon: h(ApiOutlined)
    },
    {
        tp: 'client',
        title: '用户数量',
        value: data.value?.client_list?.length ?? 0,
        icon: h(UserOutlined)
    }
])

watchEffect(async () => {
    try {
        const resp = await reqBaseStat()
        if (resp.code === 200) data.value = resp.data
        else message.error(resp.msg)
    } catch {
        message.error('获取数据失败')
    }
})

// 统计数据
const todayVisits = ref(0);
const todayVisitors = ref(0);
const todayNewUsers = ref(0);
const avgVisitsPerUser = computed(() => {
    return todayVisitors.value ? todayVisits.value / todayVisitors.value : 0;
});

// 中国地图相关
const chinaMapRef = ref();
let chinaMap: echarts.ECharts | null = null;

// 添加一个基础的地图数据
const baseMapData = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": { "name": "中国" },
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[[[73.88, 39.77], [135.08, 39.77], [135.08, 3.51], [73.88, 3.51], [73.88, 39.77]]]]
            }
        }
    ]
};

// 修改 onMounted 函数
onMounted(async () => {
    try {
        // 首先尝试使用在线数据
        const response = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_simple.json', {
            mode: 'cors',  // 添加 CORS 模式
            headers: {
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const chinaJSON = await response.json();
        registerMap('china', chinaJSON);
    } catch (error) {
        console.warn('Failed to load online map data, using basic map:', error);
        // 如果在线数据加载失败，使用基础地图数据
        registerMap('china', baseMapData);
    }

    try {
        // 初始化地图
        initChinaMap();
        
        // 模拟获取数据
        todayVisits.value = 1234;
        todayVisitors.value = 567;
        todayNewUsers.value = 89;
    } catch (error) {
        console.error('Failed to initialize map:', error);
        message.error('初始化地图失败');
    }
});

// 修改地图配置，简化一些设置
const initChinaMap = () => {
    if (chinaMapRef.value) {
        chinaMap = echarts.init(chinaMapRef.value);
        const option = {
            title: {
                text: '访问地区分布',
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c}次'
            },
            series: [{
                name: '访问量',
                type: 'map',
                map: 'china',
                roam: false,  // 禁用缩放和平移
                label: {
                    show: true,
                    fontSize: 8
                },
                data: [
                    { name: '北京', value: 89 },
                    { name: '上海', value: 92 },
                    { name: '广东', value: 98 },
                    // ... 其他省份数据保持不变
                ]
            }]
        };
        chinaMap.setOption(option);
    }
};

// 监听窗口大小变化
window.addEventListener('resize', () => {
    chinaMap?.resize();
});
</script>

<style scoped>
.statistics-row {
    padding: 20px;
}

.stat-card {
    height: 120px;
    transition: all 0.3s;

    &:hover {
        transform: translateY(-2px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
}

.map-card {
    height: 100%;
    min-height: 300px;  /* 增加最小高度 */
    
    .china-map {
        height: 100%;  /* 修改为100%以充满容器 */
        min-height: 300px;
        width: 100%;
    }
}

.row1 {
    padding: 20px;

    .col {
        max-width: 300px;
        font-weight: bold;

        .card {
            cursor: pointer;
            transition: all 0.2s linear;

            &:hover {
                box-shadow: 0 0 6px rgba(0, 0, 0, 0.3);
            }
        }

        .card-active {
            background-color: #00b96b;
        }
    }
}
</style>