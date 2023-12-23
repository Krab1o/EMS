import { EventType } from 'store/events/types';

export type EventCardContainerProps = {
  initialData: EventType;
};

export enum ActionsEnum {
  LIKE = 'LIKE',
  DISLIKE = 'DISLIKE',
}
