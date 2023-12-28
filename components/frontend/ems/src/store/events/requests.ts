import { createAsyncThunk } from '@reduxjs/toolkit';
import { EventsApi } from 'services/api/events/eventsApi';
import { getEventsAdapter } from './adapters';
import {
  EventStatusEnum,
  IPostEvent,
  IVoteEvent,
} from 'services/api/events/eventsApi.type';

const getAllEvents = createAsyncThunk(
  'events/getAllEvents',
  async (status?: EventStatusEnum) => {
    const response = await EventsApi.getAllEvents(status);
    return getEventsAdapter(response);
  },
);

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

const deleteEvent = createAsyncThunk(
  'events/deleteEvent',
  async (id: number, { dispatch }) => {
    await EventsApi.deleteEvent(id);
    dispatch(getAllEvents());
  },
);

const changeEventStatus = createAsyncThunk(
  'events/approveEvent',
  async (
    { id, status }: { id: number; status: EventStatusEnum },
    { dispatch },
  ) => {
    await EventsApi.changeEventStatus(id, status);
    dispatch(getAllEvents(status));
  },
);

export { getAllEvents, postEvent, voteEvent, deleteEvent, changeEventStatus };
