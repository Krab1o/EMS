import type { RootState } from 'store';

function selectIsAuth(state: RootState) {
  return state.auth.isAuth;
}

function selectIsInit(state: RootState) {
  return state.auth.isInit;
}
function selectFetchStatus(state: RootState) {
  return state.auth.fetchStatus;
}

export { selectIsAuth, selectFetchStatus, selectIsInit };
