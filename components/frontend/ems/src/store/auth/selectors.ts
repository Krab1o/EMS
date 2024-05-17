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

function selectRole(state: RootState) {
  return state.auth.role;
}

export { selectIsAuth, selectFetchStatus, selectIsInit, selectRole };
