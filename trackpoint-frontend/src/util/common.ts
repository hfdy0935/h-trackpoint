export function copyToClipboard(text: string) {
    return navigator.clipboard.writeText(text)
}



export function deepcopy<O>(obj: O): O {
    return JSON.parse(JSON.stringify(obj))
}


