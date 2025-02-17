import L from 'leaflet'
import CompassImage from '@/assets/compass.svg'

// 地图行政区初始样式
export const initStyle = {
  fillColor: '#ccc',
  weight: 1,
  opacity: 0.7,
  color: 'white',
  fillOpacity: 1,
}
/**
 * 阿里地图选择器中国全图的code
 */
export const CHINA_CODE = 100000

/**
 * 获取阿里地图选择器中某个code的geojson，默认是全国
 * @param code
 */
export async function reqALiGeoJson(code: number) {
  return (await fetch(`https://geo.datav.aliyun.com/areas_v3/bound/${code}_full.json`)).json()
}

// 指北针
export class CompassControl extends L.Control {
  onAdd(map: L.Map): HTMLElement {
    const img = new Image()
    img.src = CompassImage
    img.width = 30
    img.height = 30
    img.classList.add('control')
    return img
  }
}

export class BackControl extends L.Control {
  cb: () => void = () => {}
  constructor({
    position = 'topleft',
    cb,
  }: {
    position?: 'topleft' | 'topright' | 'bottomleft' | 'bottomright' | undefined
    cb: () => void
  }) {
    super({ position })
    this.cb = cb
  }
  onAdd(map: L.Map): HTMLElement {
    const container = L.DomUtil.create('div', 'cb-icon leaflet-bar leaflet-control')

    const link = L.DomUtil.create('a', 'leaflet-bar-part', container)
    link.href = '#'

    L.DomEvent.on(link, 'click', this.cb)
    return container
  }
}
