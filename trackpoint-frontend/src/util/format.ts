import dayjs, { Dayjs } from 'dayjs'

export function dayjsToFormatDate(d: Dayjs) {
  return d.format('YYYY-MM-DD HH:mm:ss')
}

export function dateStrToDayjs(s: string) {
  return dayjs(s)
}

export function formateLngLat(lng: number, lat: number) {
  if (lng > 360 || lat > 90 || lng < -360 || lat < -90) {
    return ''
  }
  const _lng = lng > 0 ? `${lng}°E` : `${lng}°W`
  const _lat = lat > 0 ? `${lat}°N` : `${lat}°S`
  return `${_lng} ${_lat}`
}
