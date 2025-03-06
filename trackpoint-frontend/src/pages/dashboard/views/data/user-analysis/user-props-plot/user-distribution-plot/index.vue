<template>
    <plot-card :spinning>
        <div ref="mapRef" class="map-container">
            <div class="compass"></div>
        </div>
        <template #title>
            用户分布
            <a-tooltip title="中国区域数据来自阿里DataV">
                <question-circle-outlined />
            </a-tooltip>
        </template>
    </plot-card>
</template>

<script setup lang="ts">
import type { IClient } from '@/type/data/userAnalysis';
import { onMounted, ref, useTemplateRef, watchEffect } from 'vue';
import L, { type LeafletMouseEvent } from 'leaflet'
import { BackControl, CHINA_CODE, CompassControl, initStyle, reqALiGeoJson } from './utils';
import 'leaflet.chinatmsproviders';
import 'leaflet/dist/leaflet.css';
import 'leaflet-fullscreen'
import 'leaflet-fullscreen/dist/leaflet.fullscreen.css'
import { QuestionCircleOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import PlotCard from '@/pages/dashboard/component/plot-card.vue';

const { data } = defineProps<{
    data: IClient[]
}>()
const spinning = ref(false)
const mapRef = useTemplateRef<HTMLDivElement>('mapRef')
const map = ref<L.Map | null>(null)
let pointLayer = L.layerGroup()
watchEffect(() => {
    // 初始化一次
    if (mapRef.value && !map.value) {
        map.value = L.map(mapRef.value, {
            // @ts-ignore
            fullscreenControl: true
        }).setView([30, 110], 3)
            .addControl(L.control.scale({ 'imperial': false })).addControl(new CompassControl())
            .addControl(new BackControl({
                async cb() {
                    if (jsonCodeArr.value.length > 1) {
                        jsonCodeArr.value.pop()
                        await refreshBasemap(jsonCodeArr.value[jsonCodeArr.value.length - 1])
                    }
                }
            }))
        // @ts-ignore
        L.tileLayer.chinaProvider('GaoDe.Normal.Map').addTo(map.value);
    }
    if (map.value) {
        // 清除原来的点
        pointLayer.clearLayers()
        // 添加数据
        data.map(({ lng, lat }) => {
            L.circleMarker([lat, lng], { radius: 1 }).addTo(pointLayer)
        })
        pointLayer.addTo(map.value as L.Map)
    }
})

/* --------------------------------- geoJSON底图 -------------------------------- */
const geoJSON = ref<L.GeoJSON | null>(null)
const jsonCodeArr = ref<number[]>([]) // code栈
/**
 * 更新geoJSON底图
 * @param code 阿里地图选择器中的代码
 */
const refreshBasemap = async (code: number = CHINA_CODE) => {
    try {
        spinning.value = true
        // 获取之和再移除
        const jsonData = await reqALiGeoJson(code)
        const json = L.geoJSON(jsonData, { style: initStyle, pane: 'tilePane' }) // 放到底层
        geoJSON.value?.removeFrom(map.value as L.Map)
        geoJSON.value = json
        geoJSON.value.addTo(map.value as L.Map)
        // 适应边界
        map.value?.fitBounds(geoJSON.value.getBounds())
        // 悬浮事件
        geoJSON.value.bindTooltip(l => {
            // @ts-ignore
            const name = l.feature.properties.name
            return name
        })
    } catch {
        message.error('地图加载失败')
    } finally {
        spinning.value = false
    }
    geoJSON.value?.on({
        async click(e: LeafletMouseEvent) {
            // 如果有下一级
            if (e.sourceTarget.feature.properties.childrenNum > 0) {
                const code = e.sourceTarget.feature.properties.adcode;
                jsonCodeArr.value.push(code)
                await refreshBasemap(code)
            }
        },
        mouseout: e => e.target.setStyle(initStyle),
        mousemove(e) {
            // 类似于事件代理，找到实际触发的图层
            // 更新地图高亮
            e.sourceTarget.setStyle({
                weight: 2,
                fillColor: '#7799ff',
                dashArray: '',
                fillOpacity: 1
            });
        }
    })
}
onMounted(async () => {
    await refreshBasemap()
    jsonCodeArr.value.push(CHINA_CODE)
})
</script>

<style scoped>
.map-container {
    width: 100%;
    height: 540px;
    position: relative;

    .compass {
        width: 20px;
        height: 20px;
        position: absolute;
        top: 0;
        right: 0;
        background-image: url(/trackpoint-frontend/src/assets/compass.svg);
        z-index: 9999;
    }
}

:deep(.cb-icon a) {
    background-image: url(/src/assets/back.svg);
    background-size: contain;
}
</style>