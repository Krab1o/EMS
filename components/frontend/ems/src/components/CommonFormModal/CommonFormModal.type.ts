import type { FormInstance } from 'antd';
import type { ColumnType } from 'antd/es/table/interface';
import type { IField, IModalState } from 'shared/types/types';

export interface CommonFormModalProps<T> {
  columns: Array<ColumnType<T> & IField>;
  modalState: IModalState;
  form: FormInstance<T>;
  disabledSave: boolean;
  handleCancel: () => void;
  onSubmit: (values: T) => void;
  handleReset: () => void;
  handleFormChange: () => void;
}
