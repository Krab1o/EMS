import type { SelectProps } from 'antd';
import type { IOption, ITableParams } from 'shared/types/types';

export interface IApiEntity {
  id: number;
  title: string;
}
export interface AsyncSelectProps
  extends Omit<SelectProps<IOption | IOption[]>, 'options' | 'children'> {
  fetchOptions: (tableParams?: ITableParams) => Promise<Array<IApiEntity>>;
  debounceTimeout?: number;
}
