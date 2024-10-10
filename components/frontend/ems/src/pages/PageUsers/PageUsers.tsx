import { useCallback, useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { useAppDispatch } from 'store';
import {
  deleteUser,
  getUsers,
  selectCurrentUser,
  selectPage,
  selectUsers,
  userActions,
} from 'store/users';
import { Button, Modal, Space, Table, Pagination } from 'antd';
import { DeleteOutlined, EyeOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import type { UserType } from 'store/users/types';
import styles from './PageUsers.module.scss';

export default function PageUsers() {
  const dispatch = useAppDispatch();
  const usersData = useSelector(selectUsers);
  const currentPage = useSelector(selectPage);
  const currentUser = useSelector(selectCurrentUser);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<UserType | null>(null);

  useEffect(() => {
    dispatch(getUsers(currentPage));
  }, [currentPage, dispatch]);

  const handleViewUser = useCallback((user: UserType) => {
    setSelectedUser(user);
    setIsViewModalOpen(true);
  }, []);

  const handleDeleteUser = useCallback(
    (user: UserType) => {
      dispatch(userActions.setCurrentUser(user));
    },
    [dispatch],
  );

  const confirmDeleteUser = useCallback(() => {
    if (currentUser) {
      dispatch(deleteUser({ id: currentUser.id, page: currentPage }));
      dispatch(userActions.setCurrentUser(null));
    }
  }, [currentUser, currentPage, dispatch]);

  const closeViewModal = () => {
    setIsViewModalOpen(false);
    setSelectedUser(null);
  };

  const columns: ColumnsType<UserType> = [
    {
      title: 'Имя',
      dataIndex: 'firstName',
      key: 'firstName',
    },
    {
      title: 'Фамилия',
      dataIndex: 'lastName',
      key: 'lastName',
    },
    {
      title: 'Действия',
      key: 'actions',
      render: (user: UserType) => (
        <Space>
          <Button type={'link'} onClick={() => handleViewUser(user)}>
            <EyeOutlined />
          </Button>
          <Button type={'link'} danger onClick={() => handleDeleteUser(user)}>
            <DeleteOutlined />
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div className={styles.pageContainer}>
      <div className={styles.tableContainer}>
        <Table
          columns={columns}
          dataSource={usersData}
          rowKey="id"
          pagination={false}
          scroll={{ x: 'max-content' }} // Позволяет таблице быть адаптивной на мобильных устройствах
        />
        <Pagination
          current={currentPage}
          total={usersData.length}
          onChange={(page) => dispatch(getUsers(page))}
          className={styles.pagination}
        />
      </div>
      <Modal
        title="Информация о пользователе"
        visible={isViewModalOpen}
        onCancel={closeViewModal}
        footer={[
          <Button key="close" onClick={closeViewModal}>
            Закрыть
          </Button>,
        ]}
      >
        {selectedUser && (
          <div>
            <p>
              <strong>Имя:</strong> {selectedUser.firstName}
            </p>
            <p>
              <strong>Фамилия:</strong> {selectedUser.lastName}
            </p>
            <p>
              <strong>Отчество:</strong> {selectedUser.middleName}
            </p>
            <p>
              <strong>Факультет:</strong> {selectedUser.institution.title}
            </p>
            <p>
              <strong>Курс:</strong> {selectedUser.course ?? 'N/A'}
            </p>
            <p>
              <strong>Номер группы:</strong> {selectedUser.group ?? 'N/A'}
            </p>
            <p>
              <strong>Роль:</strong> {selectedUser.role}
            </p>
          </div>
        )}
      </Modal>

      <Modal
        title="Удаление пользователя"
        visible={currentUser !== null}
        onOk={confirmDeleteUser}
        onCancel={() => dispatch(userActions.setCurrentUser(null))}
        okText="Да"
        cancelText="Отмена"
        okButtonProps={{ danger: true }}
      >
        Вы уверены, что хотите удалить пользователя {currentUser?.firstName}{' '}
        {currentUser?.lastName}?
      </Modal>
    </div>
  );
}
