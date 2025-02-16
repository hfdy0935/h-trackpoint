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

// 检查地图数据是否加载
const checkMapExists = () => {
    if (!echarts.getMap('china')) {
        // 如果地图数据未加载，从 URL 加载
        fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
            .then(response => response.json())
            .then(geoJson => {
                echarts.registerMap('china', geoJson);
                initChinaMap();
            })
            .catch(error => {
                console.error('Failed to load map data:', error);
                message.error('加载地图数据失败');
            });
    } else {
        initChinaMap();
    }
};

onMounted(() => {
    checkMapExists();
    // 模拟数据
    todayVisits.value = 1234;
    todayVisitors.value = 567;
    todayNewUsers.value = 89;
});

// 修改地图配置
const initChinaMap = () => {
    if (chinaMapRef.value) {
        chinaMap = echarts.init(chinaMapRef.value);
        const option = {
            title: {
                text: '访问地区分布',
                left: 'center',
                top: 10,
                textStyle: {
                    fontSize: 16
                }
            },
            visualMap: {
                min: 0,
                max: 100,
                left: 'left',
                bottom: 20,
                text: ['高', '低'],
                calculable: true,
                inRange: {
                    color: ['#e0ffff', '#006edd']
                }
            },
            series: [{
                name: '访问量',
                type: 'map',
                map: 'china',
                roam: true,
                zoom: 1.2,  
                layoutCenter: ['50%', '50%'],  
                layoutSize: '95%',  
                label: {
                    show: true,
                    fontSize: 10,  
                    color: '#333',
                    position: 'inside',  
                    distance: 3,  
                    formatter: '{b}',  
                    align: 'center',
                    verticalAlign: 'middle',
                    backgroundColor: 'rgba(255,255,255,0.5)',  
                    padding: [2, 4],  
                },
                itemStyle: {
                    areaColor: '#e0ffff',
                    borderColor: '#fff',  
                    borderWidth: 1.5,     
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 12,
                        fontWeight: 'bold',
                        backgroundColor: 'rgba(255,255,255,0.8)'
                    },
                    itemStyle: {
                        areaColor: '#006edd',
                        shadowBlur: 10,
                        shadowColor: 'rgba(0,0,0,0.3)'
                    }
                },
                data: [
                    { name: '北京', value: 89 },
                    { name: '天津', value: 45 },
                    { name: '上海', value: 92 },
                    { name: '重庆', value: 56 },
                    { name: '河北', value: 67 },
                    { name: '河南', value: 75 },
                    { name: '云南', value: 43 },
                    { name: '辽宁', value: 68 },
                    { name: '黑龙江', value: 52 },
                    { name: '湖南', value: 78 },
                    { name: '安徽', value: 63 },
                    { name: '山东', value: 89 },
                    { name: '浙江', value: 88 },
                    { name: '江西', value: 52 },
                    { name: '湖北', value: 73 },
                    { name: '广西', value: 59 },
                    { name: '甘肃', value: 44 },
                    { name: '山西', value: 53 },
                    { name: '陕西', value: 61 },
                    { name: '吉林', value: 51 },
                    { name: '福建', value: 71 },
                    { name: '贵州', value: 48 },
                    { name: '广东', value: 98 },
                    { name: '青海', value: 41 },
                    { name: '西藏', value: 34 },
                    { name: '四川', value: 76 },
                    { name: '宁夏', value: 42 },
                    { name: '海南', value: 49 }
                ]
            }]
        };
        chinaMap.setOption(option);
        
        // 添加窗口大小改变时的自适应
        window.addEventListener('resize', () => {
            chinaMap?.resize();
        });
    }
};
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
    min-height: 450px;
    
    .china-map {
        height: 100%;
        min-height: 450px;
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