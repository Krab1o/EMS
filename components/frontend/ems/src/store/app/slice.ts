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
  },
});

export default appSlice;
