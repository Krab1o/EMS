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
  {
    label: 'Рассмотрение',
    key: 'on_review',
    icon: <QuestionCircleOutlined />,
  },
];

export function EventPageSubheader({ openModal }: EventPageSubheaderProps) {
  const dispatch = useAppDispatch();
  const currentStatus = useSelector(selectCurrentEventsStatus);

  const onClick: MenuProps['onClick'] = (e) => {
    dispatch(eventsActions.setCurrentEventsStatus(e.key as EventStatusEnum));
    dispatch(getAllEvents(e.key as EventStatusEnum));
  };

  return (
    <div className={styles.header}>
      <Menu
        onClick={onClick}
        selectedKeys={[currentStatus]}
        mode="horizontal"
        items={items}
      ></Menu>
      <Button icon={<PlusOutlined />} onClick={openModal} />
    </div>
  );
}
