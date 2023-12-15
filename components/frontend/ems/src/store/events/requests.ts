import { createAsyncThunk } from '@reduxjs/toolkit';
import { EventsApi } from 'services/api/eventsApi';
import { getEventsAdapter } from './adapters';
import { IPostEvent } from 'services/api/api.type';

const getAllEvents = createAsyncThunk('events/getAllEvents', async () => {
  const response = await EventsApi.getAllEvents();
  return getEventsAdapter(response);
});

const postEvent = createAsyncThunk(
  'events/postEvent',
  async (data: IPostEvent, { dispatch }) => {
    await EventsApi.postEvent(data);
    dispatch(getAllEvents());
  },
);

export { getAllEvents, postEvent };
