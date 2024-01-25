import type { RootState } from 'store';

function selectModalState(state: RootState) {
  return state.app.modalState;
}

export { selectModalState };
