import type { RootState } from 'store';

function selectModalState(state: RootState) {
  return state.app.modalState;
}

function selectAlert(state: RootState) {
  return state.app.alert;
}

export { selectModalState, selectAlert };
