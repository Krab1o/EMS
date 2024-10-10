import { useEffect, useState } from 'react';
import { useAppDispatch } from 'store';
import { getAllEvents, selectEvents } from 'store/events';
import { useSelector } from 'react-redux';
import { selectRole } from 'store/auth';
import EventCardContainer from 'containers/EventCardContainer';
import EventPageSubheader from 'containers/EventPageSubheader';
import CreateEventModalContainer from 'containers/CreateEventModalContainer';
import { EventStatusEnum } from 'services/api/events/eventsApi.type';
import { AdminEvents } from 'components/AdminEvents/AdminEvents';
import { Row, Col } from 'antd';

// Импортируем стили
import styles from './PageEvents.module.scss';

export function PageEvents() {
  const dispatch = useAppDispatch();
  const events = useSelector(selectEvents);
  const role = useSelector(selectRole);

  const [isCreateEventModalOpen, setIsCreateModalOpen] =
    useState<boolean>(false);

  useEffect(() => {
    dispatch(getAllEvents(EventStatusEnum.OnPoll));
  }, [dispatch]);

  const openModal = () => {
    setIsCreateModalOpen(true);
  };

  return (
    <div>
      {/* Используем адаптированные стили для заголовка */}
      <div className={styles.header}>
        <EventPageSubheader openModal={openModal} role={role} />
      </div>

      <CreateEventModalContainer
        open={isCreateEventModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
      />

      <div className={styles.content}>
        {role === 'admin' ? (
          <AdminEvents events={events} />
        ) : (
          <Row gutter={[16, 16]} justify="center" style={{ marginTop: '5%' }}>
            {events &&
              events.map((el) => (
                <Col key={el.id}>
                  <EventCardContainer initialData={el} />
                </Col>
              ))}
          </Row>
        )}
      </div>
    </div>
  );
}
