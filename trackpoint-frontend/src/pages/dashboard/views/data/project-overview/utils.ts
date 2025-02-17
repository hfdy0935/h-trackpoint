/**
 * 根据0-1计算颜色
 * @param rate
 */
export function calcColorFromRate(rate: number) {
  if (rate < 0.2) return ''
  if (rate < 0.4) return '#00b96b'
  if (rate < 0.6) return '#1677FF'
  if (rate < 0.8) return '#FF7626'
  return '#f5222d'
}

/**
 * 转换时间以便显示
 * @param t
 */
export function transTime(t: string) {
  const targetDate = new Date(t)
  const currentDate = new Date()
  const timeDifference = currentDate.getTime() - targetDate.getTime()
  const secondsDifference = timeDifference / 1000

  const secondsInMinute = 60
  const secondsInHour = 60 * secondsInMinute
  const secondsInDay = 24 * secondsInHour

  if (secondsDifference < secondsInMinute) {
    const secondsAgo = Math.floor(secondsDifference)
    return `${secondsAgo} 秒`
  } else if (secondsDifference < secondsInHour) {
    const minutesAgo = Math.floor(secondsDifference / secondsInMinute)
    return `${minutesAgo} 分钟`
  } else if (secondsDifference < secondsInDay) {
    const hoursAgo = Math.floor(secondsDifference / secondsInHour)
    return `${hoursAgo} 小时`
  } else {
    const daysAgo = Math.floor(secondsDifference / secondsInDay)
    return `${daysAgo} 天`
  }
}
