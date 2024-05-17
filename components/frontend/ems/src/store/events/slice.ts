import eventsInitialState from './initialState';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import {
  checkIfPlaceFree,
  deleteEvent,
  getAllEvents,
  updateEvent,
} from './requests';
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
      state.currentEvent = null;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(getAllEvents.fulfilled, (state, action) => {
      state.events = action.payload.data;
      if (action.payload.status)
        state.currentEventsStatus = action.payload.status;
    });
    builder.addCase(deleteEvent.fulfilled, (state) => {
      state.currentEvent = null;
    });
    builder.addCase(updateEvent.fulfilled, (state) => {
      state.currentEvent = null;
    });
    builder.addCase(checkIfPlaceFree.fulfilled, (state, action) => {
      state.isPlaceFree = action.payload;
    });
    builder.addCase(checkIfPlaceFree.rejected, (state) => {
      state.isPlaceFree = false;
    });
  },
});

export default eventsSlice;
