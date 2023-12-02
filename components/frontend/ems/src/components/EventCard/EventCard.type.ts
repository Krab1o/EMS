import { EventType } from 'store/events/types';

export type EventCardProps = {
  initialData: EventType;
  onCardClick: () => void;
};
