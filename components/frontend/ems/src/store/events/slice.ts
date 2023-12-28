import eventsInitialState from './initialState';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { getAllEvents } from './requests';
import { EventType } from './types';
import { EventStatusEnum } from 'services/api/events/eventsApi.type';

const eventsSlice = createSlice({
  name: 'events',
  initialState: eventsInitialState,
  reducers: {
    setCurrentEvent: (state, action: PayloadAction<EventType>) => {
      state.currentEvent = action.payload;
    },
    setCurrentEventsStatus: (state, action: PayloadAction<EventStatusEnum>) => {
      state.currentEventsStatus = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(getAllEvents.fulfilled, (state, action) => {
      state.events = action.payload;
    });
  },
});

export default eventsSlice;
