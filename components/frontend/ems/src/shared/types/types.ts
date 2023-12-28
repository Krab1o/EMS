import type { ReactNode } from 'react';
import type { Rule } from 'rc-field-form/lib/interface';
import type { IApiEntity } from 'components/AsyncSelect/AsyncSelect.type';
import type { AnyObject } from 'antd/es/_util/type';

export interface IOption {
  value: string;
  label: ReactNode;
}

export interface IPagination {
  page: number;
  size: number;
}

export interface ITableParams {
  pagination?: IPagination;
}

export interface IWithPagination<T> {
  count: number;
  next: null | string;
  previous: string;
  results: Array<T>;
}

export type FieldTypes =
  | 'input'
  | 'number'
  | 'select'
  | 'date'
  | 'datetime'
  | 'checkbox'
  | 'asyncSelect';

export interface IField {
  formField?: {
    fieldType?: FieldTypes;
    rules?: Array<Rule>;
    selectFields?: Array<{
      label: ReactNode;
      value: string | number | boolean;
    }>;
    fetchOptions?: (tableParams?: ITableParams) => Promise<Array<IApiEntity>>;
    isSelectMulti?: boolean;
  };
}

export enum ModalType {
  CREATE = 'create',
  UPDATE = 'update',
  FILTER = 'filter',
  VIEWING = 'viewing',
  COLUMNS = 'columns',
}

export interface IModalState {
  isOpen: boolean;
  modalType: null | ModalType;
  initialData: null | AnyObject;
  title: string;
}
