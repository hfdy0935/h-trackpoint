import dayjs, { Dayjs } from "dayjs";


export function dayjsToFormatDate(d: Dayjs) {
    return d.format('YYYY-MM-DD HH:mm:ss')
}

export function dateStrToDayjs(s: string) {
    return dayjs(s)
}