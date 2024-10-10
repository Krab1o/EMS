import { useAppDispatch } from 'store';
import { useSelector } from 'react-redux';
import {
  eventsActions,
  getAllEvents,
  selectCurrentEventsStatus,
} from 'store/events';

import { Button, Menu, Select } from 'antd';
import {
  ClockCircleOutlined,
  FireOutlined,
  PlusOutlined,
  QuestionCircleOutlined,
  CalculatorFilled,
} from '@ant-design/icons';

import type { EventPageSubheaderProps } from './EventPageSubheader.type';
import { EventStatusEnum } from 'services/api/events/eventsApi.type';

import styles from './EventPageSubheader.module.scss';
import { useEffect, useState } from 'react';

export function EventPageSubheader({
  openModal,
  role,
}: EventPageSubheaderProps) {
  const dispatch = useAppDispatch();
  const currentStatus = useSelector(selectCurrentEventsStatus);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  // Обновляем состояние при изменении размера экрана
  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 768);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const onClick = (key: EventStatusEnum) => {
    dispatch(eventsActions.setCurrentEventsStatus(key));
    dispatch(getAllEvents(key));
  };

  const getItems = (role: string | null) => {
    const items = [
      {
        label: 'Запланированные',
        key: EventStatusEnum.Planned,
        icon: <ClockCircleOutlined />,
      },
      {
        label: 'Голосование',
        key: EventStatusEnum.OnPoll,
        icon: <FireOutlined />,
      },
    ];
    if (role === 'admin') {
      items.push({
        label: 'Рассмотрение',
        key: EventStatusEnum.OnReview,
        icon: <QuestionCircleOutlined />,
      });
      items.push({
        label: 'Завершенные',
        key: EventStatusEnum.Ended,
        icon: <CalculatorFilled />,
      });
    }

    return items;
  };

  const items = getItems(role).map((item) => ({
    label: item.label,
    value: item.key,
  }));

  return (
    <div className={styles.header}>
      {/* Горизонтальное меню для десктопной версии */}
      {!isMobile ? (
        <Menu
          disabledOverflow={true}
          onClick={(e) => onClick(e.key as EventStatusEnum)}
          selectedKeys={[currentStatus]}
          mode="horizontal"
          items={getItems(role)}
        />
      ) : (
        // Выпадающий список для мобильной версии
        <Select
          defaultValue={currentStatus}
          onChange={onClick}
          options={items}
          className={styles.dropdown_mobile}
        />
      )}

      <Button
        className={styles.header__button_desktop}
        icon={<PlusOutlined />}
        onClick={openModal}
      />
    </div>
  );
}
