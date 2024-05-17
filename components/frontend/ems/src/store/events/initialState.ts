import type { EventType } from './types';
import { EventStatusEnum } from 'services/api/events/eventsApi.type';

const eventsInitialState = {
  events: null as null | Array<EventType>,
  currentEvent: null as null | EventType,
  currentEventsStatus: 'on_poll' as EventStatusEnum,
  isPlaceFree: true,
};

export default eventsInitialState;
