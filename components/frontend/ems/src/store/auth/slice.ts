import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { postLoginData } from './requests';
import authInitialState from './initialState';

const authSlice = createSlice({
  name: 'auth',
  initialState: authInitialState,
  reducers: {
    setIsAuth: (state, action: PayloadAction<boolean>) => {
      state.isAuth = action.payload;
    },
    setIsInit: (state, action: PayloadAction<boolean>) => {
      state.isInit = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(postLoginData.pending, (state) => {
        state.fetchStatus = {
          isLoading: true,
          error: '',
        };
      })
      .addCase(postLoginData.fulfilled, (state) => {
        state.fetchStatus = {
          isLoading: false,
          error: '',
        };
        state.isAuth = true;
        state.isInit = true;
      })
      .addCase(postLoginData.rejected, (state, { error }) => {
        state.isAuth = false;
        state.fetchStatus = {
          isLoading: false,
          error: String(error.message),
        };
      });
  },
});

export default authSlice;
