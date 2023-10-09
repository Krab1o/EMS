import { configureStore } from '@reduxjs/toolkit';
import { useDispatch } from 'react-redux';

type RootState = ReturnType<typeof store.getState>;
type AppDispatch = typeof store.dispatch;

const store = configureStore({
  reducer: {},
  devTools: process.env.REACT_APP_ENV === 'dev',
});

const useAppDispatch = () => useDispatch<AppDispatch>();
export type { RootState, AppDispatch };
export { store as default, useAppDispatch };
