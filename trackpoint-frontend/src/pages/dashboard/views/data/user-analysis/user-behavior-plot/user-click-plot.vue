<template>
    <plot-card :spinning title="各页面点击热力图">
        <template #title>
            <a-tooltip title="数据来自上传的默认click事件">
                <question-circle-outlined />
            </a-tooltip>
            点击热力图
        </template>
        <template #extra>
            <a-button type="text" @click="isHeatmapFullscreen = true">
                <fullscreen-outlined />
            </a-button>
        </template>
        <a-row>
            <a-col>
                <a-form-item label="页面链接" style="margin-left: 20px;" :colon="false">
                    <a-select v-model:value="queryClick.url" style="width: 200px;margin-left: 10px;" placeholder="选择页面"
                        :options="clickOptions" :field-names="{ label: 'url', value: 'url' }">
                    </a-select>
                </a-form-item>
            </a-col>
            <a-col>
                <a-form-item label="页面大小" style="margin-left: 20px;" :colon="false">
                    <a-select v-model:value="queryClick.wh" style="width: 200px;margin-left: 10px;" placeholder="选择宽高">
                        <a-select-option v-for="([w, h]) in whOptions" :key="`${w}${h}`" :value="`${w}_${h}`">
                            {{ w }} × {{ h }}
                        </a-select-option>
                    </a-select>
                </a-form-item>
            </a-col>
            <a-col>
                <a-form-item label="不透明度" style="margin-left: 20px;" :colon="false">
                    <a-slider v-model:value="opacity" style="width: 160px;"></a-slider>
                </a-form-item>
            </a-col>
            <a-col>
                <a-form-item label="热点大小" style="margin-left: 20px;" :colon="false">
                    <a-slider v-model:value="size" style="width: 160px;"></a-slider>
                </a-form-item>
            </a-col>
        </a-row>
        <a-empty v-if="!spinning && clickData.xy?.length === 0"></a-empty>
        <user-click-plot-heatmap :clickData v-if="!spinning && clickData.xy?.length > 0" :opacity :size/>
        <a-modal v-model:open="isHeatmapFullscreen" :closable="false" wrap-class-name="full-modal" width="100%">
            <user-click-plot-heatmap :clickData v-if="!spinning && clickData.xy?.length > 0" :opacity :size/>
        </a-modal>
    </plot-card>
</template>

<script setup lang="ts">
import { reqUserClickData } from '@/api/v1/data/userAnalysis';
import PlotCard from '@/pages/dashboard/component/plot-card.vue';
import type { ReqUserBehaviorAnalysis, RespClickRecord, RespUserBehaviorAnalysis } from '@/type/data/userAnalysis';
import { QuestionCircleOutlined, FullscreenOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { computed, ref, watch, watchEffect } from 'vue';
import UserClickPlotHeatmap from './user-click-plot-heatmap.vue';

const { data: clickOptions, query: queryProjEvtTime } = defineProps<{
    data: RespUserBehaviorAnalysis['click']
    query: ReqUserBehaviorAnalysis
}>()
// 选择的页面和宽高
interface QueryClick {
    url: string
    wh: string
}
const queryClick = ref<QueryClick>({} as QueryClick)
// 能选的宽高选项
const whOptions = computed<[number, number][]>(() => clickOptions.find(c => c.url === queryClick.value.url)?.wh ?? [])
// 有页面和宽高选项时自动选择第一个
watch(() => clickOptions, newValue => {
    if (newValue.length) {
        const firstPage = newValue[0]
        queryClick.value.url = firstPage.url
        if (firstPage.wh.length) {
            queryClick.value.wh = firstPage.wh[0].join('_')
        }
    }
})
// 页面url变化时（新旧都有值，表示切换，不是初始化），如果新的页面有大小选项就选第一个，否则清空宽高选项和已有数据
watch(() => queryClick.value.url, (newValue, oldValue) => {
    if (newValue && oldValue) {
        queryClick.value.wh = whOptions.value.length > 0 ? whOptions.value[0].join('_') : ''
        clickData.value = {} as RespClickRecord
    }
})
// 要显示的点击坐标数据
const clickData = ref<RespClickRecord>({} as RespClickRecord)
const spinning = ref(false)
watchEffect(async () => {
    if (queryClick.value.url && queryClick.value.wh && queryProjEvtTime.projectId && queryProjEvtTime.eventId) {
        const [w, h] = queryClick.value.wh.split('_')
        try {
            spinning.value = true
            const resp = await reqUserClickData({
                ...queryProjEvtTime,
                url: queryClick.value.url,
                width: +w,
                height: +h,
            })
            if (resp.code === 200) {
                clickData.value = resp.data
            } else {
                message.error(resp.msg)
            }
        } catch {
            message.error('获取点击数据失败')
        } finally {
            spinning.value = false
        }
    }
})

// 是否全屏显示热力图
const isHeatmapFullscreen = ref(false)
// 不透明度
const opacity = ref(60)
// 大小
const size = ref(20)
</script>


<style>
.full-modal {
    .ant-modal {
        max-width: 100%;
        top: 0;
        padding-bottom: 0;
        margin: 0;
    }

    .ant-modal-content {
        display: flex;
        flex-direction: column;
        height: calc(100vh);
    }

    .ant-modal-body {
        flex: 1;
    }
}
</style>