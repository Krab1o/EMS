import { useEffect, useState } from 'react';
import { useAppDispatch } from 'store';
import { useNavigate } from 'react-router-dom';
import { EventsApi } from 'services/api/events/eventsApi';
import {
  deleteEvent,
  eventsActions,
  updateEvent,
  voteEvent,
} from 'store/events';
import EventCard from 'components/EventCard';
import {
  ActionsEnum,
  EventCardContainerProps,
} from './EventCardContainer.type';
import { EventStatusEnum } from 'services/api/events/eventsApi.type';

export function EventCardContainer({ initialData }: EventCardContainerProps) {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const [image, setImage] = useState('');
  const onCardClick = () => {
    dispatch(eventsActions.setCurrentEvent(initialData));
    navigate(`${initialData.id}`);
  };

  useEffect(() => {
    if (initialData.cover)
      EventsApi.getEventImage(initialData.cover.uri).then((res) =>
        setImage(URL.createObjectURL(res)),
      );
  }, [initialData.cover]);

  const onActionsClick = (type: ActionsEnum) => {
    dispatch(
      voteEvent({ eventId: initialData.id, like: type === ActionsEnum.LIKE }),
    );
  };

  const onDelete = () => {
    dispatch(deleteEvent({ id: initialData.id, status: initialData.status }));
  };
  const onApprove = () => {
    dispatch(
      updateEvent({
        id: initialData.id,
        status: EventStatusEnum.OnPoll,
        cover: initialData.cover,
        datetime: initialData.date.toISOString(),
        description: initialData.description,
        // place: initialData.place,
        title: initialData.title,
        user_vote: initialData.userVote,
        version: initialData.version + 1,
        voted_no: initialData.votedNo,
        voted_yes: initialData.votedYes,
      }),
    );
  };

  return (
    <EventCard
      initialData={initialData}
      onCardClick={onCardClick}
      onActionsClick={onActionsClick}
      onDelete={onDelete}
      image={image}
      onApprove={onApprove}
    />
  );
}
