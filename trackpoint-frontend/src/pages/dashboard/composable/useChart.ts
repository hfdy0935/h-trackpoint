import { Chart } from '@antv/g2'
import type { RuntimeOptions } from '@antv/g2/lib/api/runtime'

import { onBeforeUnmount, onMounted, useTemplateRef, watchEffect, type Ref } from 'vue'

interface UseChartProps {
  refName: string
  options?: RuntimeOptions
  cb?(chart: Chart): void
}
export function useChart(props: UseChartProps): {
  refName: string
  domRef: Ref<HTMLElement | null>
  chart: Chart | null
  getChart(): Chart | null
} {
  const { refName, options = {}, cb } = props
  const domRef = useTemplateRef<HTMLElement>(refName)
  let chart: Chart | null = null
  watchEffect(() => {
    if (domRef.value) {
      chart = new Chart({
        container: domRef.value!,
        autoFit: true,
        ...options,
      })
      chart.clear()
      cb?.(chart)
    }
  })
  onBeforeUnmount(() => {
    chart?.destroy()
  })

  return {
    refName,
    domRef,
    chart,
    getChart() {
      return chart
    },
  }
}
