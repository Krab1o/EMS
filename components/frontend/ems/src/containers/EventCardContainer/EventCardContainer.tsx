import { useEffect, useState } from 'react';
import { useAppDispatch } from 'store';
import { useNavigate } from 'react-router-dom';
import { EventsApi } from 'services/api/events/eventsApi';
import { deleteEvent, eventsActions, voteEvent } from 'store/events';
import EventCard from 'components/EventCard';
import {
  ActionsEnum,
  EventCardContainerProps,
} from './EventCardContainer.type';

export function EventCardContainer({ initialData }: EventCardContainerProps) {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const [image, setImage] = useState('');
  const onCardClick = () => {
    dispatch(eventsActions.setCurrentEvent(initialData));
    navigate(`${initialData.id}`);
  };

  useEffect(() => {
    EventsApi.getEventImage(initialData.cover.uri).then((res) =>
      setImage(URL.createObjectURL(res)),
    );
  }, [initialData.cover.uri]);

  const onActionsClick = (type: ActionsEnum) => {
    dispatch(
      voteEvent({ eventId: initialData.id, like: type === ActionsEnum.LIKE }),
    );
  };

  const onDelete = () => {
    dispatch(deleteEvent(initialData.id));
  };

  return (
    <EventCard
      initialData={initialData}
      onCardClick={onCardClick}
      onActionsClick={onActionsClick}
      onDelete={onDelete}
      image={image}
    />
  );
}
