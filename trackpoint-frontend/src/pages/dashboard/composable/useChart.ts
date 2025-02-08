import { Chart } from "@antv/g2";
import { onMounted, useTemplateRef } from "vue";

export function useChart(refName: string) {
    const domRef = useTemplateRef<HTMLElement>(refName)
    let chart: Chart | null = null
    onMounted(() => {
        chart = new Chart({
            container: domRef.value!,
            autoFit: true,
        })
    })
    return { domRef, chart }
}