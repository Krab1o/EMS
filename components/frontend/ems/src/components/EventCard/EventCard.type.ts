import { EventType } from 'store/events/types';
import { ActionsEnum } from 'containers/EventCardContainer/EventCardContainer.type';

export type EventCardProps = {
  initialData: EventType;
  onCardClick: () => void;
  onActionsClick: (type: ActionsEnum) => void;
};
