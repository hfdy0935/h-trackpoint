<template>
    <div class="container">
        <h-tools>
            <template #before>
                <a-tooltip :title="isFullscreen ? '退出全屏' : '全屏'">
                    <component :is="isFullscreen ? FullscreenExitOutlined : FullscreenOutlined"
                        @click="toggleFullscreen" style="margin-right: 10px;" />
                </a-tooltip>
            </template>
        </h-tools>
        <a-dropdown>
            <div class="welcome">
                <a>
                    {{ user.nickname }}
                    <down-outlined />
                </a>
            </div>
            <template #overlay>
                <a-menu>
                    <a-menu-item @click="open = true; op = 'user-info'">
                        个人信息
                    </a-menu-item>
                    <a-menu-item @click="open = true; op = 'update-pwd'">
                        修改密码
                    </a-menu-item>
                    <a-menu-item @click="open = true; op = 'logout'">
                        <a-popconfirm title="确定要退出登录吗？" @confirm="logout" ok-text="确定" cancel-text="取消"
                            placement="bottomRight">
                            退出登录
                        </a-popconfirm>
                    </a-menu-item>
                </a-menu>
            </template>
        </a-dropdown>
    </div>
    <a-modal v-if="op !== 'logout'" v-model:open="open" :title="MenuOpTitle[op]" :closable="false" :footer="null">
        <component :is="MenuOpComp[op]" />
    </a-modal>
</template>

<script setup lang="ts">
import HTools from '@/components/header/h-tools.vue';
import { useUserStore } from '@/store';
import { storeToRefs } from 'pinia';
import { DownOutlined, FullscreenExitOutlined, FullscreenOutlined } from '@ant-design/icons-vue'
import UserInfo from './user-info.vue';
import UpdatePassword from './update-password.vue';
import { ref } from 'vue';
import { message } from 'ant-design-vue';

const { user } = storeToRefs(useUserStore())
const { logout } = useUserStore()
const open = ref(false)
type MenuOp = 'user-info' | 'update-pwd' | 'logout'
const MenuOpComp: {
    [k in Exclude<MenuOp, 'logout'>]: any
} = {
    'user-info': UserInfo,
    'update-pwd': UpdatePassword
}
const MenuOpTitle: {
    [k in Exclude<MenuOp, 'logout'>]: any
} = {
    'user-info': '个人信息',
    'update-pwd': '修改密码'
}
const op = ref<MenuOp>('user-info')

const isFullscreen = ref(false)
const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
        // 进入全屏
        document.documentElement.requestFullscreen().catch(err => {
            message.error('不支持全屏')
        });
        isFullscreen.value = true;
    } else {
        // 退出全屏
        document.exitFullscreen().catch(err => {
            message.error(`退出全屏失败`);
        });
        isFullscreen.value = false;
    }
}
</script>

<style scoped>
.container {
    width: 100%;
    height: 60px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    box-shadow: 5px 1px 6px #cccccc;

    .welcome {
        width: 80px;
        margin-left: 10px;
        font-size: 14px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }

}
</style>