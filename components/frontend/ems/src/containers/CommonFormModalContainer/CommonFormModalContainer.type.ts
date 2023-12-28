import type { ColumnType } from 'antd/es/table/interface';
import type { IField } from 'shared/types/types';

export interface CommonFormModalContainerProps<T> {
  columns: Array<ColumnType<T> & IField>;
  onSubmit: (values: T) => void;
}
