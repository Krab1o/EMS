import { createAsyncThunk } from '@reduxjs/toolkit';
import { EventsApi } from 'services/api/events/eventsApi';
import { getEventsAdapter } from './adapters';
import { eventsActions } from 'store/events/actions';
import {
  EventStatusEnum,
  IEvent,
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
    dispatch(getAllEvents(EventStatusEnum.OnReview));
    dispatch(eventsActions.setCurrentEventsStatus(EventStatusEnum.OnReview));
  },
);

const voteEvent = createAsyncThunk(
  'events/voteEvent',
  async (data: IVoteEvent, { dispatch }) => {
    await EventsApi.voteEvent(data);
    dispatch(getAllEvents(EventStatusEnum.OnPoll));
  },
);

const deleteEvent = createAsyncThunk(
  'events/deleteEvent',
  async (
    { id, status }: { id: number; status: EventStatusEnum },
    { dispatch },
  ) => {
    await EventsApi.deleteEvent(id);
    dispatch(getAllEvents(status));
  },
);

const updateEvent = createAsyncThunk(
  'events/updateEvent',
  async (event: IEvent, { dispatch }) => {
    await EventsApi.updateEvent(event);
    dispatch(getAllEvents(event.status));
  },
);

// const changeEventStatus = createAsyncThunk(
//   'events/approveEvent',
//   async (
//     { id, status }: { id: number; status: EventStatusEnum },
//     { dispatch },
//   ) => {
//     await EventsApi.changeEventStatus(id, status);
//     dispatch(getAllEvents(status));
//   },
// );

export { getAllEvents, postEvent, voteEvent, deleteEvent, updateEvent };
