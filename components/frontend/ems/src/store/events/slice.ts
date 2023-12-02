import eventsInitialState from './initialState';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { getAllEvents } from './requests';
import { EventType } from './types';

const eventsSlice = createSlice({
  name: 'events',
  initialState: eventsInitialState,
  reducers: {
    setCurrentEvent: (state, action: PayloadAction<EventType>) => {
      state.currentEvent = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(getAllEvents.fulfilled, (state, action) => {
      state.events = action.payload;
    });
  },
});

export default eventsSlice;
