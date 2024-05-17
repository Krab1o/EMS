import { useAppDispatch } from 'store';
import { useSelector } from 'react-redux';
import {
  eventsActions,
  getAllEvents,
  selectCurrentEventsStatus,
} from 'store/events';

import { Button, Menu, MenuProps } from 'antd';
import {
  ClockCircleOutlined,
  FireOutlined,
  PlusOutlined,
  QuestionCircleOutlined,
} from '@ant-design/icons';

import type { EventPageSubheaderProps } from './EventPageSubheader.type';
import { EventStatusEnum } from 'services/api/events/eventsApi.type';

import styles from './EventPageSubheader.module.scss';

export function EventPageSubheader({
  openModal,
  role,
}: EventPageSubheaderProps) {
  const dispatch = useAppDispatch();
  const currentStatus = useSelector(selectCurrentEventsStatus);

  const onClick: MenuProps['onClick'] = (e) => {
    dispatch(eventsActions.setCurrentEventsStatus(e.key as EventStatusEnum));
    dispatch(getAllEvents(e.key as EventStatusEnum));
  };

  const getItems = (role: string | null) => {
    const items: MenuProps['items'] = [
      {
        label: 'Запланированные',
        key: 'planned',
        icon: <ClockCircleOutlined />,
      },
      {
        label: 'Голосование',
        key: 'on_poll',
        icon: <FireOutlined />,
      },
    ];
    if (role === 'admin')
      items.push({
        label: 'Рассмотрение',
        key: 'on_review',
        icon: <QuestionCircleOutlined />,
      });
    return items;
  };

  return (
    <div className={styles.header}>
      <Menu
        onClick={onClick}
        selectedKeys={[currentStatus]}
        mode="horizontal"
        items={getItems(role)}
      ></Menu>
      <Button
        className={styles.header__button_desktop}
        icon={<PlusOutlined />}
        onClick={openModal}
      />
      <Button
        type={'link'}
        className={styles.header__button_mobile}
        onClick={openModal}
      >
        Добавить
      </Button>
    </div>
  );
}
