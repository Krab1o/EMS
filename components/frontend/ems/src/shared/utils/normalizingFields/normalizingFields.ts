import { isValid, parseISO } from 'date-fns';
import type { AnyObject } from 'antd/es/_util/type';

export function deNormalize(values: AnyObject | null) {
  const init: AnyObject = {};
  if (values) {
    Object.entries(values).forEach(([key, value]) => {
      const timeValue = parseISO(value);
      if (value && isValid(new Date(value)) && isValid(timeValue)) {
        init[key] = new Date(parseISO(value));
      } else {
        init[key] = value;
      }
    });
  }
  return init;
}

export function normalize<T>(values: T) {
  const finishValues: AnyObject = {};
  Object.entries(values as AnyObject).forEach(([key, value]) => {
    if (typeof value?.getMonth === 'function') {
      finishValues[key] = value ? value.toISOString() : undefined;
    } else {
      finishValues[key] = value;
    }
  });
  return finishValues;
}
