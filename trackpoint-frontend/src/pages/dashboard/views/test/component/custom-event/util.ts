import type { IEvent } from '@/type/event'
import yaml from 'js-yaml'

export function genJSONStrFromIEvent(e: IEvent) {
  const data = Object.fromEntries(
    e.param_list.map((p) => [
      p.name,
      p.type === 'number'
        ? 0
        : p.type === 'string'
          ? ''
          : p.type === 'boolean'
            ? false
            : p.type === 'array'
              ? []
              : p.type === 'object'
                ? {}
                : null,
    ]),
  )
  return JSON.stringify(data, null, 2)
}

export function genYAMLStrFromIEvent(e: IEvent) {
  return yaml.dump(JSON.parse(genJSONStrFromIEvent(e)), { indent: 2, flowLevel: -1 })
}

export function JSONToYAML(s: string) {
  return yaml.dump(JSON.parse(s), { indent: 2, flowLevel: -1 })
}
export function YAMLToJSON(s: string) {
  return JSON.stringify(yaml.load(s), null, 2)
}
