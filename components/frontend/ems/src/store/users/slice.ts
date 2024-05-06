import usersInitialState from './initialState';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { getUsers } from './requests';
import { UserType } from './types';

const usersSlice = createSlice({
  name: 'users',
  initialState: usersInitialState,
  reducers: {
    updatePage: (state, action: PayloadAction<number>) => {
      state.page = action.payload;
    },
    setCurrentUser: (state, action: PayloadAction<UserType | null>) => {
      state.currentUser = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(getUsers.fulfilled, (state, action) => {
      state.users = action.payload;
    });
  },
});

export default usersSlice;
