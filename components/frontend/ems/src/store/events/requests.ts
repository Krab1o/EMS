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
import { RootState } from 'store/index';
import { appActions } from 'store/app';

const getAllEvents = createAsyncThunk(
  'events/getAllEvents',
  async (status: EventStatusEnum | undefined = undefined, { getState }) => {
    const { auth } = getState() as RootState;
    const newStatus =
      auth.role !== 'admin' && status === EventStatusEnum.OnReview
        ? EventStatusEnum.OnPoll
        : status;
    const response = await EventsApi.getAllEvents(newStatus);
    return {
      data: getEventsAdapter(response),
      status: newStatus,
    };
  },
);

const postEvent = createAsyncThunk(
  'events/postEvent',
  async (data: IPostEvent, { dispatch }) => {
    await EventsApi.postEvent(data);
    dispatch(getAllEvents(EventStatusEnum.OnReview));
    dispatch(eventsActions.setCurrentEventsStatus(EventStatusEnum.OnReview));
    dispatch(
      appActions.setAlert({
        message: 'Мероприятие создано и отправлено на проверку',
        isError: false,
      }),
    );
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
    dispatch(
      appActions.setAlert({
        message: 'Мероприятие удалено',
        isError: false,
      }),
    );
  },
);

const updateEvent = createAsyncThunk(
  'events/updateEvent',
  async (event: IEvent, { dispatch }) => {
    await EventsApi.updateEvent(event);
    dispatch(
      appActions.setAlert({
        message: 'Мероприятие успешно изменено',
        isError: false,
      }),
    );
    dispatch(getAllEvents(event.status));
  },
);

export { getAllEvents, postEvent, voteEvent, deleteEvent, updateEvent };
