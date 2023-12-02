import { getClient } from './axios';
import { IEvent } from './api.type';

export const EventsApi = {
  async getAllEvents() {
    const response = await getClient().get<Array<IEvent>>('/events');
    return response.data;
  },
};
