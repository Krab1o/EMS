import { EventType } from './types';

const eventsInitialState = {
  events: null as null | Array<EventType>,
  currentEvent: null as null | EventType,
};

export default eventsInitialState;
