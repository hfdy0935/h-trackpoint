<template>
    <a-tooltip title="过滤参数">
        <filter-outlined style="margin-left: 10px;font-size: large;" @click="open = true" />
    </a-tooltip>
    <a-modal v-model:open="open" :closable="false" @ok="doFilter" cancel-text="重置"
        :ok-button-props="{ style: { backgroundColor: '#00b96b' } }">
        <template #title>
            过滤参数
            <a-tooltip title="目前只支持逻辑且">
                <question-circle-outlined style="margin-left: 6px;" />
            </a-tooltip>
        </template>
        <div class="param-title">
            <span>参数名</span>
            <span>参数值</span>
        </div>
        <div class="event-param-form-container">
            <a-form>
                <a-form-item :colon="false" v-for="(param, index) in data" :key="index" label="">
                    <div class="event-param">
                        <a-input v-model:value="param.name" class="input" allow-clear></a-input>
                    </div>
                </a-form-item>
            </a-form>
            <a-form>
                <a-form-item :colon="false" v-for="(param, index) in data" :key="index" label="">
                    <div class="event-param">
                        <a-input v-model:value="param.value" class="input" allow-clear></a-input>
                        <minus-circle-outlined class="minus-icon" @click="removeItem(index)" />
                    </div>
                </a-form-item>
            </a-form>
        </div>
        <a-form-item>
            <a-button type="dashed" @click="addItem">
                <plus-outlined />
                添加参数
            </a-button>
        </a-form-item>
    </a-modal>
</template>

<script setup lang="ts">
import { useRecordStore } from '@/store';
import type { IFilterParam } from '@/type/record';
import { deepcopy } from '@/util/common';
import { FilterOutlined, MinusCircleOutlined, QuestionCircleOutlined, PlusOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';

const open = ref(false)
const { query } = storeToRefs(useRecordStore())
const data = ref<IFilterParam[]>([])
const addItem = () => {
    const nameList = data.value.map(d => d.name)
    if (nameList.includes('')) {
        message.warning('参数名不能为空')
        return
    }
    if (nameList.length !== new Set(nameList).size) {
        message.warning('参数名不能重复')
        return
    }
    data.value.push({
        name: '',
        value: ''
    })
}
const removeItem = (index: number) => {
    data.value.splice(index, 1)
}

const doFilter = () => {
    if (data.value.some(d => !d)) {
        message.warning('参数名不能为空')
        return
    }
    query.value.filterParamList = deepcopy(data.value)
}

const doReset = () => {
    data.value = []
    if (query.value.filterParamList.length !== 0)
        query.value.filterParamList = []
}
</script>


<style scoped>
.param-title {
    width: 100%;
    display: flex;
    justify-content: space-evenly;
    margin: 30px 0;


    :not(:last-child) {
        width: 120px;
    }

    :nth-child(3) {
        width: 56px;
    }
}

.event-param-form-container {
    display: flex;
    justify-content: space-around;

    .event-param {
        display: flex;
        justify-content: space-evenly;

        .input {
            width: 120px;
        }

        .minus-icon {
            transform: translateX(15px);

            &:hover {
                color: red
            }
        }

    }
}
</style>