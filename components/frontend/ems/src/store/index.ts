import { configureStore } from '@reduxjs/toolkit';
import { useDispatch } from 'react-redux';
import eventsSlice from 'store/events';
import authSlice from 'store/auth';
import appSlice from 'store/app';
import sectionsSlice from './sections';
import usersSlice from './users';

type RootState = ReturnType<typeof store.getState>;
type AppDispatch = typeof store.dispatch;

const store = configureStore({
  reducer: {
    events: eventsSlice.reducer,
    auth: authSlice.reducer,
    app: appSlice.reducer,
    sections: sectionsSlice.reducer,
    users: usersSlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ serializableCheck: false }),
  devTools: true,
});

const useAppDispatch = () => useDispatch<AppDispatch>();
export type { RootState, AppDispatch };
export { store as default, useAppDispatch };
