<template>
    <project-event-selector @change="change">
        <template #extra>
            <a-form-item label="时间" :colon="false">
                <a-range-picker style="margin-left:10px;width: 330px;" show-time @change="changeDate"
                    :allowEmpty="[true, true]" />
            </a-form-item>
        </template>
    </project-event-selector>
    <a-row>
        <a-col :span="24">
            <pv-uv-plot :data="data.visit" :spinning />
        </a-col>
        <a-col :span="24" :xl="12">
            <user-click-plot :data="data.click" :query />
        </a-col>
        <a-col :span="24" :xl="12">
            <user-stay-plot :data="data.stay" :spinning />
        </a-col>
    </a-row>
</template>


<script lang="ts" setup>
import { reqUserBehaviorAnalysis } from '@/api/v1/data/userAnalysis';
import type { TimePeriod } from '@/type/base';
import type { ReqUserBehaviorAnalysis, RespUserBehaviorAnalysis } from '@/type/data/userAnalysis';
import { message } from 'ant-design-vue';
import { ref, watchEffect } from 'vue';
import ProjectEventSelector from '~dashboard/component/project-event-selector.vue'
import PvUvPlot from './pv-uv-plot.vue';
import type { Dayjs } from 'dayjs';
import UserClickPlot from './user-click-plot.vue';
import UserStayPlot from './user-stay-plot.vue';


const query = ref<ReqUserBehaviorAnalysis>({
    projectId: '',
    eventId: '',
    timePeriod: {}
})
const data = ref<RespUserBehaviorAnalysis>({
    visit: [], click: [], stay: []
})
const spinning = ref(false)
const change = async (projectId: string, eventId: string) => {
    query.value.projectId = projectId
    query.value.eventId = eventId
}
watchEffect(async () => {
    if (!query.value.projectId || !query.value.eventId) {
        data.value = {
            visit: [], click: [], stay: []
        }
        return
    }
    try {
        spinning.value = true
        const resp = await reqUserBehaviorAnalysis(query.value)
        if (resp.code === 200) data.value = resp.data
        else message.error(resp.msg)
    } catch {
        message.error('获取用户信息失败')
    } finally {
        spinning.value = false
    }
})
const changeDate = async (_: [Dayjs, Dayjs] | [string, string], dateStrings: [string, string]) => {
    query.value.timePeriod = {
        start: dateStrings[0] || undefined,
        end: dateStrings[1] || undefined
    }
}
</script>