import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { useAppDispatch } from 'store';
import { appActions, selectModalState } from 'store/app';

import CommonFormModal from 'components/CommonFormModal';
import { Form } from 'antd';

import type { CommonFormModalContainerProps } from './CommonFormModalContainer.type';
import type { NamePath } from 'rc-field-form/lib/interface';
import { ModalType } from 'shared/types/types';

export default function CommonFormModalContainer<T>({
  columns,
  onSubmit,
}: CommonFormModalContainerProps<T>) {
  const dispatch = useAppDispatch();
  const modalState = useSelector(selectModalState);
  const [disabledSave, setDisabledSave] = useState(true);
  const [form] = Form.useForm<T>();

  function handleFormChange() {
    let isValid = true;
    const hasErrors = form.getFieldsError().some(({ errors }) => errors.length);
    if (!hasErrors)
      columns.forEach(({ dataIndex, formField }) => {
        const formValue = form.getFieldValue(dataIndex as NamePath);
        const isFindRule =
          formField &&
          formField.rules?.find(
            (rule) => typeof rule === 'object' && rule.required,
          );

        const isCreatingRequired =
          modalState.modalType === ModalType.CREATE && isFindRule;

        const isUpdatingRequired =
          modalState.modalType === ModalType.UPDATE && isFindRule;

        if (
          formValue === undefined &&
          (isCreatingRequired || isUpdatingRequired)
        )
          isValid = false;
      });
    setDisabledSave(hasErrors || !isValid);
  }

  function onReset() {
    setDisabledSave(true);
  }

  function handleCancel() {
    setDisabledSave(true);
    dispatch(
      appActions.setIsModalOpen({
        title: '',
        modalType: null,
        isOpen: false,
        initialData: null,
      }),
    );
  }

  function onSubmitForm(values: T) {
    if (modalState.initialData) {
      onSubmit({ ...values, pk: modalState.initialData.pk });
    } else {
      onSubmit(values);
    }
    handleCancel();
  }

  useEffect(() => {
    if (modalState.modalType) form.resetFields();
  }, [form, modalState.initialData, modalState.modalType]);

  if (modalState.modalType)
    return (
      <CommonFormModal<T>
        columns={columns}
        disabledSave={disabledSave}
        modalState={modalState}
        form={form}
        handleCancel={handleCancel}
        onSubmit={onSubmitForm}
        handleFormChange={handleFormChange}
        handleReset={onReset}
      />
    );
  return null;
}
