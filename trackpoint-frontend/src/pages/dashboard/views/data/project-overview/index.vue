<template>
    <a-row>
        <a-col v-for="(item, i) in [...data, ...data, ...data, ...data, ...data, ...data, ...data]" :key="item.id"
            :span="24" :md="12" :xl="8" :xxl="6" style="padding: 16px;">
            <plot-card>
                <template #title>
                    <div style="display: flex;align-items: center;">
                        <a-tooltip :title="item.status === StatusEnum.NORMAL ? '状态正常' : '已停用'">
                            <div style="width: 100px;display: flex; align-items: center;">
                                <div class="status"
                                    :style="{ backgroundColor: item.status === StatusEnum.NORMAL ? '#00b96b' : 'red' }">
                                </div>
                                {{ item.name }}
                            </div>
                        </a-tooltip>
                        <a-tag style="margin-left: 20px;">已运行 {{ transTime(item.create_time) }}</a-tag>
                    </div>
                </template>
                <template #extra>
                    <a-tooltip title="管理项目" @click="router.push('/project')">
                        <setting-outlined class="icon" />
                    </a-tooltip>
                    <a-tooltip title="管理上报记录" @click="router.push('/record')">
                        <send-outlined class="icon" />
                    </a-tooltip>
                </template>
                <div class="count-row">
                    <a-statistic>
                        <template #title>
                            <user-outlined /> 用户量
                        </template>
                        <template #formatter>
                            <span>{{ item.client_count }}</span>
                        </template>
                    </a-statistic>
                    <a-statistic :value="item.record_count">
                        <template #title>
                            <book-outlined /> 上报记录/条
                        </template>
                    </a-statistic>
                </div>
                <div class="count-row">
                    <a-statistic>
                        <template #title>
                            <api-outlined
                                :style="{ color: (item.default_count + item.custom_count) / user.eventNumLimit > 0.8 ? 'red' : '' }" />
                            事件用量
                        </template>
                        <template #formatter>
                            <a-progress type="circle" size="small"
                                :percent="(item.default_count + item.custom_count) * 100 / user.eventNumLimit"
                                :success="{ percent: item.default_count * 100 / user.eventNumLimit }" />
                        </template>
                    </a-statistic>
                    <a-statistic>
                        <template #title>
                            <api-outlined /> 默认/自定义事件
                        </template>
                        <template #formatter>
                            {{ item.default_count }} / {{ item.custom_count }}
                        </template>
                    </a-statistic>
                </div>
                <div class="count-row">
                    <a-statistic>
                        <template #title>
                            <clock-circle-outlined
                                :style="{ color: item.performance_total_time > 500 * 0.8 ? 'red' : '' }" /> 页面加载时间
                        </template>
                        <template #formatter>
                            <span :style="{ color: calcColorFromRate(item.performance_total_time / 500) }">
                                {{ item.performance_total_time >= 0 ? item.performance_total_time.toFixed(2) + 'ms' : ''
                                }}
                            </span>
                        </template>
                    </a-statistic>
                    <a-statistic>
                        <template #title>
                            <folder-open-outlined :style="{ color: item.performance_js_rate > 0.8 ? 'red' : '' }" />
                            JS占用内存
                        </template>
                        <template #formatter>
                            <span :style="{ color: calcColorFromRate(item.performance_js_rate) }">
                                {{ item.performance_js_rate >= 0 ? (item.performance_js_rate * 100).toFixed(2) + '%' :
                                    ''
                                }}
                            </span>
                        </template>
                    </a-statistic>
                </div>
                <div class="count-row">
                    <a-statistic>
                        <template #title>
                            <alert-outlined :style="{ color: item.request_error_rate > 0.8 ? 'red' : '' }" /> 网络请求报错率
                        </template>
                        <template #formatter>
                            <span :style="{ color: calcColorFromRate(item.request_error_rate) }">{{
                                item.request_error_rate >= 0 ? (item.request_error_rate
                                    * 100).toFixed(2) + '%' : '' }}</span>
                        </template>
                    </a-statistic>
                    <a-statistic>
                        <template #title>
                            <alert-outlined :style="{ color: item.js_error_count > 500 * 0.8 ? 'red' : '' }" /> JS报错
                        </template>
                        <template #formatter>
                            <span :style="{ color: calcColorFromRate(item.js_error_count / 500) }">{{
                                item.js_error_count >= 0 ? `${item.js_error_count}次` : ''
                            }}</span>
                        </template>
                    </a-statistic>
                </div>
            </plot-card>
        </a-col>
    </a-row>
</template>

<script setup lang="ts">
import { SideMenuNameEnum, StatusEnum } from '@/enum';
import { useUserStore } from '@/store';
import { ApiOutlined, AlertOutlined, FolderOpenOutlined, UserOutlined, BookOutlined, ClockCircleOutlined, SettingOutlined, SendOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { storeToRefs } from 'pinia';
import { watchEffect } from 'vue';
import { ref } from 'vue';
import { reqProjectStat } from '@/api/v1/data/projectStat';
import { calcColorFromRate, transTime } from './utils';
import { useRouter } from 'vue-router';
import type { IProjectStat } from '@/type/data/projectstat';
import PlotCard from '@/pages/dashboard/component/plot-card.vue';


defineOptions({
    name: SideMenuNameEnum.ProjectOverview
})

const router = useRouter()
const { user } = storeToRefs(useUserStore())
const data = ref<IProjectStat[]>([])

watchEffect(async () => {
    try {
        const resp = await reqProjectStat()
        if (resp.code === 200) data.value = resp.data
        else message.error(resp.msg)
    } catch {
        message.error('获取项目信息失败')
    }
})

</script>

<style scoped>
.status {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin: 0 8px;
}


.count-row {
    display: flex;
    justify-content: space-evenly;

    div {
        margin: 10px 0;
        width: 40%;
    }
}

.icon {
    margin-left: 10px;

    &:hover {
        color: #1677FF;
    }
}
</style>
