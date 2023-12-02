import { Button, Menu, MenuProps } from 'antd';
import React, { useState } from 'react';
import {
  ClockCircleOutlined,
  FireOutlined,
  PlusOutlined,
  QuestionCircleOutlined,
} from '@ant-design/icons';
import styles from './EventPageSubheader.module.scss';
import { EventPageSubheaderProps } from './EventPageSubheader.type';

const items: MenuProps['items'] = [
  {
    label: 'Запланированные',
    key: 'planned',
    icon: <ClockCircleOutlined />,
  },
  {
    label: 'Голосование',
    key: 'vote',
    icon: <FireOutlined />,
  },
  {
    label: 'Рассмотрение',
    key: 'review',
    icon: <QuestionCircleOutlined />,
  },
];

export function EventPageSubheader({ openModal }: EventPageSubheaderProps) {
  const [current, setCurrent] = useState('planned');
  const onClick: MenuProps['onClick'] = (e) => {
    setCurrent(e.key);
  };

  return (
    <div className={styles.header}>
      <Menu
        onClick={onClick}
        selectedKeys={[current]}
        mode="horizontal"
        items={items}
      ></Menu>
      <Button icon={<PlusOutlined />} onClick={openModal} />
    </div>
  );
}
