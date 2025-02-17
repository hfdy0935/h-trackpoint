import type { IClient } from '@/type/data/userAnalysis'
import L from 'leaflet'

interface IData {
  points: IClient[]
  jsonData: any[]
}
// TODO 计算每个行政区的点的数量
// 每个行政区有多少个点的缓存
const pointNumInAreaCacheMap = new Map<number, number>()

self.addEventListener('message', async ({ data }: { data: IData }) => {
  // 计算每个多边形点的数量
  const { points, jsonData } = data
  //   const geoJson = L.geoJSON(jsonData)
  //   geoJson.eachLayer((p) => {
  //     const code = p.feature.properties.adcode
  //     if (pointNumInAreaCacheMap.has(code)) return
  //     pointNumInAreaCacheMap.set(code, points.filter(({ lng, lat }) => p.contains([lat, lng])).length)
  //   })
  self.postMessage(pointNumInAreaCacheMap)
})
