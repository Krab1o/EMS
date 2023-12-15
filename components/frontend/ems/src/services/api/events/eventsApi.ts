import { getClient } from 'services/api/axios';
import type {
  IEvent,
  IPostEvent,
  IVoteEvent,
} from 'services/api/events/eventsApi.type';

export const EventsApi = {
  async getAllEvents() {
    const response = await getClient().get<Array<IEvent>>('/events');
    return response.data;
  },
  async postEvent(data: IPostEvent) {
    const response = await getClient().post<IEvent>('/events', data);
    return response.data;
  },
  async voteEvent(data: IVoteEvent) {
    const response = await getClient().post(`/events/${data.eventId}/vote`, {
      like: data.like,
    });
    return response.data;
  },
};
