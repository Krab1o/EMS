import type { EventType } from 'store/events/types';

export interface AdminEventsProps {
  events: Array<EventType> | null;
}
