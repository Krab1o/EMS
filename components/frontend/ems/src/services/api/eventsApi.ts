import { getClient } from './axios';
import { IEvent, IPostEvent, IVoteEvent } from './api.type';

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
