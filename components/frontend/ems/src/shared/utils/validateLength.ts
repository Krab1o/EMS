export function validateLenght(value: string, maxLength: number) {
  if (value?.length > maxLength) {
    return value.slice(0, maxLength) + '...';
  }
  return value;
}
