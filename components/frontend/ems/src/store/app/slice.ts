import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import appInitialState from './initialState';
import type { IModalState } from 'shared/types/types';

const appSlice = createSlice({
  name: 'app',
  initialState: appInitialState,
  reducers: {
    setIsModalOpen: (state, action: PayloadAction<IModalState>) => {
      state.modalState = action.payload;
    },
    setAlert: (
      state,
      action: PayloadAction<{ message: string; isError: boolean }>,
    ) => {
      state.alert = action.payload;
    },
  },
});

export default appSlice;
