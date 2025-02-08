<template>
    <a-list item-layout="horizontal" :data-source="data">
        <template #renderItem="{ item }">
            <a-list-item>
                <div class="key">{{ item.title }}</div>
                <div class="value">
                    <template v-if="item.title === '用户名'">
                        <a-input v-if="isEditing" v-model:value="user.nickname" :ref="(el: any) => el?.focus()"
                            @blur="doUpdateNickname" allow-clear></a-input>
                        <span v-else>{{ item.value }}</span>
                        <edit-outlined v-if="!isEditing" class="icon" @click="isEditing = true" />
                    </template>
                    <template v-else>{{ item.value }}</template>
                </div>
            </a-list-item>
        </template>
    </a-list>
</template>

<script setup lang="ts">
import { useUserStore } from '@/store';
import { storeToRefs } from 'pinia';
import { computed, ref } from 'vue';
import { EditOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { reqUpdateUserInfo } from '@/api/v1/user';


const { user } = storeToRefs(useUserStore())
const data = computed(() => {
    return [
        {
            title: '用户名',
            value: user.value.nickname,
        },
        {
            title: '邮箱',
            value: user.value.email,
        },
        {
            title: '注册时间',
            value: user.value.createTime
        },
        {
            title: '项目数量',
            value: `${user.value.projectNum} / ${user.value.projectNumLimit}`,
        },
        {
            title: '事件数量',
            value: `${user.value.eventNum} / ( ${user.value.projectNumLimit} * ${user.value.eventNumLimit} )`,
        }
    ]
})
const isEditing = ref(false)// 是否正在编辑用户名
const doUpdateNickname = async () => {
    try {
        const resp = await reqUpdateUserInfo({ 'nickname': user.value.nickname })
        if (resp.code === 200) message.success('修改成功')
        else message.error(resp.msg)
    } catch {
        message.error('修改失败')
    }
    finally {
        isEditing.value = false
    }
}
</script>

<style scoped>
.value {
    width: 240px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;

    .icon {
        margin-left: 6px;
        cursor: pointer;
    }
}
</style>