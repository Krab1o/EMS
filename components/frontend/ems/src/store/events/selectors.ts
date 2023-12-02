import { RootState } from 'store';

function selectEvents(state: RootState) {
  return state.events.events;
}

function selectCurrentEvent(state: RootState) {
  return state.events.currentEvent;
}

export { selectEvents, selectCurrentEvent };
