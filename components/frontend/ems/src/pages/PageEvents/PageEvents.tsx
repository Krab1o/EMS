import { useEffect, useState } from 'react';
import { useAppDispatch } from 'store';
import { getAllEvents, selectEvents } from 'store/events';
import { useSelector } from 'react-redux';
import { Flex } from 'antd';
import EventCardContainer from 'containers/EventCardContainer';
import EventPageSubheader from 'containers/EventPageSubheader';
import CreateEventModalContainer from 'containers/CreateEventModalContainer';
import { EventStatusEnum } from 'services/api/events/eventsApi.type';

export function PageEvents() {
  const dispatch = useAppDispatch();
  const events = useSelector(selectEvents);

  const [isCreateEventModalOpen, setIsCreateModalOpen] =
    useState<boolean>(false);

  useEffect(() => {
    dispatch(getAllEvents(EventStatusEnum.OnPoll));
  }, [dispatch]);

  const openModal = () => {
    setIsCreateModalOpen(true);
  };

  return (
    <div style={{ height: '100%' }}>
      <EventPageSubheader openModal={openModal} />
      <CreateEventModalContainer
        open={isCreateEventModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
      />
      <Flex
        wrap={'wrap'}
        gap={'middle'}
        justify={'center'}
        style={{ marginTop: '3%', height: '100%' }}
      >
        {events && events.map((el) => <EventCardContainer initialData={el} />)}
      </Flex>
    </div>
  );
}
