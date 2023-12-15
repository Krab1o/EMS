import { useAppDispatch } from 'store';
import { useNavigate } from 'react-router-dom';
import { eventsActions, voteEvent } from 'store/events';
import EventCard from 'components/EventCard';
import {
  ActionsEnum,
  EventCardContainerProps,
} from './EventCardContainer.type';

export function EventCardContainer({ initialData }: EventCardContainerProps) {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const onCardClick = () => {
    dispatch(eventsActions.setCurrentEvent(initialData));
    navigate(`${initialData.id}`);
  };

  const onActionsClick = (type: ActionsEnum) => {
    dispatch(
      voteEvent({ eventId: initialData.id, like: type === ActionsEnum.LIKE }),
    );
  };

  return (
    <EventCard
      initialData={initialData}
      onCardClick={onCardClick}
      onActionsClick={onActionsClick}
    />
  );
}
