/* eslint-disable no-console */
import { useCallback, useState } from 'react';
import { useAppDispatch } from 'store';
import { appActions } from 'store/app';

import { Button, Input, Modal, Space, Table } from 'antd';
import { DeleteOutlined, EditOutlined, EyeOutlined } from '@ant-design/icons';
import CommonFormModalContainer from 'containers/CommonFormModalContainer';

import type { ColumnsType } from 'antd/es/table';
import type { IUser } from 'pages/PageUsers/PageUsers.type';
import { columns } from 'pages/PageUsers/PageUsers.constants';
import { ModalType } from 'shared/types/types';

import styles from './PageUsers.module.scss';

export default function PageUsers() {
  const [deletedUser, setDeletedUser] = useState<IUser | null>(null);
  const dispatch = useAppDispatch();
  const data: IUser[] = [
    {
      key: '1',
      username: 'Olga112',
      firstname: 'Ольга',
      lastname: 'Архипова',
      surname: 'Дмитриевна',
      role: 'Студент',
      id: 1,
    },
    {
      key: '2',
      username: 'Hvost@229',
      firstname: 'Олег',
      lastname: 'Потапов',
      surname: 'Дмитриевич',
      role: 'Студент',
      id: 2,
    },
    {
      key: '3',
      username: 'Olga990',
      firstname: 'Ольга',
      lastname: 'Архипова',
      surname: 'Дмитриевна',
      role: 'Студент',
      id: 3,
    },
    {
      key: '4',
      username: 'Motilek',
      firstname: 'Матвей',
      lastname: 'Архипов',
      surname: 'Дмитриевич',
      role: 'Студент',
      id: 4,
    },
  ];
  const columnsWithActions: ColumnsType<IUser> = [
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
                `Редактирование пользователя ${record.username}`,
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
                `Просмотр пользователя ${record.username}`,
              )
            }
          >
            <EyeOutlined />
          </Button>
          <Button onClick={() => setDeletedUser(record)} type={'link'} danger>
            <DeleteOutlined />
          </Button>
        </Space>
      ),
    },
  ];

  const handleModalOpen = useCallback(
    (modalType: ModalType | null, initialData: IUser | null, title: string) => {
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
    console.log('delete', deletedUser);
    setDeletedUser(null);
  }
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

      <Table columns={columnsWithActions} dataSource={data} />
      <Modal
        title="Удаления пользователя"
        open={deletedUser !== null}
        onOk={onDeleteUser}
        onCancel={() => setDeletedUser(null)}
        cancelText={'Отмена'}
        okText={'Да'}
        okButtonProps={{
          danger: true,
        }}
        cancelButtonProps={{
          type: 'primary',
        }}
      >
        Вы уверены, что хотите удалить пользователя {deletedUser?.username}?
      </Modal>
      <CommonFormModalContainer
        columns={columns}
        onSubmit={(data) => console.log(data)}
      />
    </div>
  );
}
