<template>
    <div class="monitor-alert-container">
      <div class="ring-gauge">
        <div class="chart-row">
        <RingGauge title="整体健康状况" :value="healthStatus" color="#91CC75" />
        <RingGauge title="JS错误占比" :value="jsErrorRatio" color="#5470C6" />
        <RingGauge title="自定义异常占比" :value="customErrorRatio" color="#EE6666" />
        <RingGauge title="静态资源异常占比" :value="resourceErrorRatio" color="#FAC858" />
        <RingGauge title="接口异常占比" :value="apiErrorRatio" color="#73C0DE" />
      </div>
      </div>

      <!-- JS 报错趋势图 -->
        <div class="line-chart">
            <LineChart title="JS 报错趋势" :data="jsErrorTrendData as [string, number][]" />
        </div>

  
      <a-tabs v-model:activeKey="activeTab">
        <a-tab-pane key="jsError" tab="JS异常">
          <a-table :dataSource="jsErrors" :columns="jsErrorColumns" :loading="loading" :pagination="false" />
        </a-tab-pane>
        <a-tab-pane key="requestError" tab="请求异常">
          <a-table :dataSource="requestErrors" :columns="requestErrorColumns" :loading="loading" :pagination="false" />
        </a-tab-pane>
      </a-tabs>
      <div class="footer">
        <a-button type="primary" @click="fetchJsErrors">点击刷新</a-button>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { SideMenuNameEnum } from '@/enum';
  import { getJsErrors, getRequestErrors } from '@/api/v1/monitor';
  import RingGauge from "./RingGauge.vue";
  import LineChart from "./LineChart.vue"; // 引入折线图组件
  
  interface JsError {
    time: string;
    count: number;
    pageUrl: string;
    reason: string;
  }
  
  interface RequestError {
    time: string;
    count: number;
    statusCode: number;
    method: string;
  }
  
  const activeTab = ref<string>('jsError');
  const jsErrors = ref<JsError[]>([]);
  const requestErrors = ref<RequestError[]>([]);
  const loading = ref<boolean>(false);
  
  const jsErrorColumns = [
    {
      title: '时间',
      dataIndex: 'time',
      width: '25%',
    },
    {
      title: '数量',
      dataIndex: 'count',
      width: '25%',
    },
    {
      title: '页面URL',
      dataIndex: 'pageUrl',
      width: '25%',
    },
    {
      title: '原因',
      dataIndex: 'reason',
      width: '25%',
    },
  ];
  const requestErrorColumns = [
    {
      title: '时间',
      dataIndex: 'time',
      width: '25%',
    },
    {
      title: '数量',
      dataIndex: 'count',
      width: '25%',
    },
    {
      title: '状态码',
      dataIndex: 'statusCode',
      width: '25%',
    },
    {
      title: '请求方法',
      dataIndex: 'method',
      width: '25%',
    },
  ];
  
  // 模拟数据
  const healthStatus = ref(85);
  const jsErrorRatio = ref(30);
  const customErrorRatio = ref(15);
  const resourceErrorRatio = ref(10);
  const apiErrorRatio = ref(25);
  
  // JS 报错趋势数据
  const jsErrorTrendData = ref([
    ['2025-02-10', 10],
    ['2025-02-11', 20],
    ['2025-02-12', 15],
    ['2025-02-13', 30],
    ['2025-02-14', 25],
    ['2025-02-15', 40],
    ['2025-02-16', 35],
  ]);
  
  // 从后端获取 JS 报错趋势数据
  //将返回的数据格式化为 [时间, 数量] 的数组形式，并赋值给 jsErrorTrendData。
  const fetchJsErrors = async () => {
    try {
      loading.value = true;
      const { data } = await getJsErrors();
      console.log('JS Errors Data:', data);
      if (Array.isArray(data)) {
        jsErrors.value = data;
      } else {
        console.error('Invalid data format:', data);
      }
    } catch (error) {
      console.error('Failed to fetch JS errors:', error);
    } finally {
      loading.value = false;
    }
  };
  
  const fetchRequestErrors = async () => {
    try {
      loading.value = true;
      const { data } = await getRequestErrors();
      console.log('Request Errors Data:', data);
      if (Array.isArray(data)) {
        requestErrors.value = data;
      } else {
        console.error('Invalid data format:', data);
      }
    } catch (error) {
      console.error('Failed to fetch request errors:', error);
    } finally {
      loading.value = false;
    }
  };
  
  onMounted(() => {
    fetchJsErrors();
    fetchRequestErrors();
  });
  
  defineOptions({
    name: SideMenuNameEnum.MonitorAlert,
  });
  </script>
  
  <style scoped>
  .monitor-alert-container {
    padding: 20px;
  }
  
  .footer {
    margin-top: 20px;
    text-align: center;
  }
  .chart-row {
    width: 100%;
    margin-bottom: 10px;
    border-radius: 10px;
    background-color: #fff;
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    }
  .line-chart {
    border-radius: 10px;
    background-color: #fff;
    padding: 10px;
    margin-top: 20px;
    display: flex;
    flex-direction: column;
  }

  
  .chart-row>div {
    flex: 1;
    margin: 0 10px;
  }
  </style>