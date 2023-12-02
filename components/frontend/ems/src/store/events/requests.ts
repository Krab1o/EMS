import { createAsyncThunk } from '@reduxjs/toolkit';
import { EventsApi } from 'services/api/eventsApi';
import { getEventsAdapter } from './adapters';

const getAllEvents = createAsyncThunk('events/getAllEvents', async () => {
  const reponse = await EventsApi.getAllEvents();
  return getEventsAdapter(reponse);
});

export { getAllEvents };
