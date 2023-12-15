import { createAsyncThunk } from '@reduxjs/toolkit';
import { EventsApi } from 'services/api/events/eventsApi';
import { getEventsAdapter } from './adapters';
import type {
  IPostEvent,
  IVoteEvent,
} from 'services/api/events/eventsApi.type';

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

const voteEvent = createAsyncThunk(
  'events/voteEvent',
  async (data: IVoteEvent, { dispatch }) => {
    await EventsApi.voteEvent(data);
    dispatch(getAllEvents());
  },
);

export { getAllEvents, postEvent, voteEvent };
