import { useCallback, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useAppDispatch } from 'store';
import { appActions } from 'store/app';
import {
  deleteUser,
  getUsers,
  selectCurrentUser,
  selectPage,
  selectUsers,
  userActions,
} from 'store/users';
import { Button, Modal, Space, Table, Input } from 'antd';
import CommonFormModalContainer from 'containers/CommonFormModalContainer';
import { DeleteOutlined, EditOutlined, EyeOutlined } from '@ant-design/icons';
import { ModalType } from 'shared/types/types';
import { columns } from './PageUsers.constants';
import type { ColumnsType } from 'antd/es/table';
import type { UserType } from 'store/users/types';

import styles from './PageUsers.module.scss';

export default function PageUsers() {
  const dispatch = useAppDispatch();
  const usersData = useSelector(selectUsers);
  const currentPage = useSelector(selectPage);
  const currentUser = useSelector(selectCurrentUser);
  // const modalState = useSelector(selectModalState);

  const columnsWithActions: ColumnsType<UserType> = [
    ...columns,
    {
      title: 'Действия',
      key: 'action',
      fixed: 'right',
      width: '200px',
      align: 'center',
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      render: (_, record) => (
        <Space>
          <Button
            type={'link'}
            onClick={() =>
              handleModalOpen(
                ModalType.UPDATE,
                record,
                `Редактирование пользователя ${record.firstName} ${record.lastName}`,
              )
            }
          >
            <EditOutlined />
          </Button>
          <Button
            type={'link'}
            onClick={() =>
              handleModalOpen(
                ModalType.VIEWING,
                record,
                `Просмотр пользователя ${record.firstName} ${record.lastName}`,
              )
            }
          >
            <EyeOutlined />
          </Button>
          <Button type={'link'} danger>
            <DeleteOutlined />
          </Button>
        </Space>
      ),
    },
  ];

  const handleModalOpen = useCallback(
    (
      modalType: ModalType | null,
      initialData: UserType | null,
      title: string,
    ) => {
      dispatch(
        appActions.setIsModalOpen({
          isOpen: true,
          modalType,
          title,
          initialData,
        }),
      );
    },
    [dispatch],
  );

  function onDeleteUser() {
    if (currentUser) {
      dispatch(deleteUser({ id: currentUser.id, page: currentPage }));
      dispatch(userActions.setCurrentUser(null));
    }
  }

  function onCloseModal() {
    dispatch(userActions.setCurrentUser(null));
  }

  // function onSubmitForm(data: UserType) {
  //   if (modalState.modalType === ModalType.CREATE) {
  //     dispatch(createUser({ page: currentPage, data: {} }));
  //   }
  // }

  useEffect(() => {
    dispatch(getUsers(currentPage));
  }, [currentPage, dispatch]);

  return (
    <div className={styles.table_block}>
      <div className={styles.btns}>
        <Button
          onClick={() =>
            handleModalOpen(ModalType.CREATE, null, 'Создание пользователя')
          }
        >
          Создать пользователя
        </Button>
        <Input.Search
          className={styles.search}
          placeholder={'Поиск'}
          allowClear
        />
      </div>

      <Table columns={columnsWithActions} dataSource={usersData} />
      <Modal
        title="Удаления пользователя"
        open={currentUser !== null}
        onOk={onDeleteUser}
        onCancel={onCloseModal}
        cancelText={'Отмена'}
        okText={'Да'}
        okButtonProps={{
          danger: true,
        }}
        cancelButtonProps={{
          type: 'primary',
        }}
      >
        Вы уверены, что хотите удалить пользователя ?
      </Modal>
      <CommonFormModalContainer
        columns={columns}
        onSubmit={
          /* eslint-disable-next-line no-console */
          (data) => console.log(data)
        }
      />
    </div>
  );
}
