import { EventType } from 'store/events/types';
import { ActionsEnum } from 'containers/EventCardContainer/EventCardContainer.type';

export type EventCardProps = {
  initialData: EventType;
  image: string;
  onCardClick: () => void;
  onActionsClick: (type: ActionsEnum) => void;
  onDelete: () => void;
  onApprove: () => void;
};
