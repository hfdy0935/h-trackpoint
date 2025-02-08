<template>
    <section>
        <a-row class="row1" justify="space-evenly">
            <a-col :span="8" class="col" v-for="({ tp, title, value, icon }, index) in topData" :key="index">
                <a-card :class="tp === activeType ? 'card-active card' : 'card'"
                    @click="activeType = (tp as ActiveType)">
                    <a-statistic :title :value>
                        <template #suffix>
                            <component :is="icon"></component>
                        </template>
                    </a-statistic>
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
import { ApiOutlined, AppstoreOutlined, UserOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { storeToRefs } from 'pinia';
import { computed, h, watchEffect, type VNode } from 'vue';
import { onMounted, ref } from 'vue';
import ProjectPlot from './project-plot.vue';
import type { RespBaseStat } from '@/type/data/stat/base';
import { reqBaseStat } from '@/api/v1/data';


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


</script>

<style scoped>
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