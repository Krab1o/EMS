import { useCallback } from 'react';
import dateFnsGenerateConfig from 'rc-picker/lib/generate/dateFns';
import {
  Button,
  Checkbox,
  DatePicker,
  Form,
  Input,
  InputNumber,
  Modal,
  Select,
  Space,
} from 'antd';
import AsyncSelect from 'components/AsyncSelect';

import type { CommonFormModalProps } from './CommonFormModal.type';
import type { ColumnType } from 'antd/es/table/interface';
import { IField, ModalType } from 'shared/types/types';
import type { NamePath, Store } from 'rc-field-form/lib/interface';
import type { AnyObject } from 'antd/es/_util/type';
import type { ReactNode } from 'react';
import { formItemLayout } from './CommonFormModal.constants';
import {
  deNormalize,
  normalize,
} from 'shared/utils/normalizingFields/normalizingFields';

const MyDatePicker = DatePicker.generatePicker<Date>(dateFnsGenerateConfig);

export default function CommonFormModal<T>({
  columns,
  handleCancel,
  modalState,
  form,
  onSubmit,
  handleReset,
  handleFormChange,
  disabledSave,
}: CommonFormModalProps<T>) {
  const renderField = ({
    formField,
    dataIndex,
    title,
  }: ColumnType<T> & IField) => {
    const fieldType = formField?.fieldType;
    switch (fieldType) {
      case 'input':
        return (
          <Form.Item
            key={String(dataIndex)}
            name={dataIndex as NamePath}
            label={title as ReactNode}
            labelAlign={'left'}
            rules={formField?.rules}
          >
            <Input allowClear />
          </Form.Item>
        );
      case 'date':
      case 'datetime':
        return (
          <Form.Item
            key={String(dataIndex)}
            name={dataIndex as NamePath}
            label={title as ReactNode}
            labelAlign={'left'}
            rules={formField?.rules}
          >
            <MyDatePicker
              showTime={fieldType === 'datetime'}
              placeholder={''}
              format={
                fieldType === 'datetime' ? 'dd.MM.yyyy HH:mm:ss' : 'dd.MM.yyyy'
              }
              style={{ width: '100%' }}
            />
          </Form.Item>
        );
      case 'select':
        return (
          <Form.Item
            key={String(dataIndex)}
            name={dataIndex as NamePath}
            label={title as ReactNode}
            labelAlign={'left'}
            rules={formField?.rules}
          >
            <Select
              mode={formField?.isSelectMulti ? 'multiple' : undefined}
              allowClear
            >
              {formField?.selectFields?.map(({ label, value }) => (
                <Select.Option key={String(value)} value={value}>
                  {label}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        );
      case 'asyncSelect':
        if (formField?.fetchOptions)
          return (
            <Form.Item
              key={String(dataIndex)}
              name={dataIndex as NamePath}
              label={title as ReactNode}
              labelAlign={'left'}
              rules={formField?.rules}
            >
              <AsyncSelect
                mode={formField.isSelectMulti ? 'multiple' : undefined}
                allowClear
                fetchOptions={formField.fetchOptions}
              />
            </Form.Item>
          );
        return null;
      case 'number':
        return (
          <Form.Item
            key={String(dataIndex)}
            name={dataIndex as NamePath}
            label={title as ReactNode}
            labelAlign={'left'}
            rules={formField?.rules}
          >
            <InputNumber style={{ width: '100%' }} />
          </Form.Item>
        );
      case 'checkbox':
        return (
          <Form.Item
            key={String(dataIndex)}
            name={dataIndex as NamePath}
            label={title as ReactNode}
            labelAlign={'left'}
            rules={formField?.rules}
          >
            <Checkbox />
          </Form.Item>
        );
      default:
        return null;
    }
  };

  const onFinish = useCallback(
    (values: T) => {
      const finishValues: AnyObject = normalize(values);
      onSubmit(finishValues);
    },
    [onSubmit],
  );

  return (
    <Modal
      title={modalState.title}
      open={modalState.isOpen}
      footer={null}
      onCancel={handleCancel}
      forceRender
    >
      <Form
        {...formItemLayout}
        labelWrap
        colon={false}
        initialValues={deNormalize(modalState.initialData) as Store}
        form={form}
        name={'tableForm'}
        onFieldsChange={handleFormChange}
        onFinish={onFinish}
        scrollToFirstError
        disabled={modalState.modalType === ModalType.VIEWING}
      >
        {columns.map((field) => renderField(field))}
        <Space>
          {modalState.modalType !== ModalType.VIEWING && (
            <>
              <Form.Item>
                <Button htmlType={'submit'} disabled={disabledSave}>
                  Применить
                </Button>
              </Form.Item>
              <Form.Item>
                <Button htmlType={'reset'} onClick={handleReset}>
                  Очистить
                </Button>
              </Form.Item>
              <Form.Item>
                <Button onClick={handleCancel}>Закрыть</Button>
              </Form.Item>
            </>
          )}
        </Space>
      </Form>
      {modalState.modalType === ModalType.VIEWING && (
        <div>
          <Button onClick={handleCancel}>Закрыть</Button>
        </div>
      )}
    </Modal>
  );
}
