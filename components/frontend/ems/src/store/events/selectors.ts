import { RootState } from 'store';

function selectEvents(state: RootState) {
  return state.events.events;
}

function selectCurrentEvent(state: RootState) {
  return state.events.currentEvent;
}

function selectCurrentEventsStatus(state: RootState) {
  return state.events.currentEventsStatus;
}

export { selectEvents, selectCurrentEvent, selectCurrentEventsStatus };
