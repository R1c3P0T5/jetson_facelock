import { computed } from 'vue'

export function useInvalid(props: { invalid?: boolean }, attrs: Record<string, unknown>) {
  return computed(
    () => props.invalid || attrs['aria-invalid'] === true || attrs['aria-invalid'] === 'true',
  )
}
