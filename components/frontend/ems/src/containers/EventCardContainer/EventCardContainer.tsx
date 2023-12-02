import { useAppDispatch } from 'store';
import { useNavigate } from 'react-router-dom';
import { eventsActions } from 'store/events';
import EventCard from 'components/EventCard';
import { EventCardContainerProps } from './EventCardContainer.type';

export function EventCardContainer({ initialData }: EventCardContainerProps) {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const onCardClick = () => {
    dispatch(eventsActions.setCurrentEvent(initialData));
    navigate(`${initialData.id}`);
  };
  return <EventCard initialData={initialData} onCardClick={onCardClick} />;
}
