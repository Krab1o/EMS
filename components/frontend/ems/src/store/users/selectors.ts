import { RootState } from 'store';

function selectUsers(state: RootState) {
  return state.users.users;
}

function selectCurrentUser(state: RootState) {
  return state.users.currentUser;
}

function selectPage(state: RootState) {
  return state.users.page;
}

export { selectUsers, selectCurrentUser, selectPage };
