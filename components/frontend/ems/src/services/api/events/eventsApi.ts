import { getClient } from 'services/api/axios';
import {
  EventStatusEnum,
  IEvent,
  IEventType,
  IPostEvent,
  IVoteEvent,
} from 'services/api/events/eventsApi.type';
import { ITableParams } from 'shared/types/types';

export const EventsApi = {
  async getAllEvents(status?: EventStatusEnum) {
    const params = new URLSearchParams();
    if (status) params.append('event_status', status);
    const response = await getClient().get<Array<IEvent>>('/events?' + params);
    return response.data;
  },
  async postEvent(data: IPostEvent) {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('place', data.place);
    formData.append('datetime', data.datetime);
    formData.append('description', data.description);
    formData.append('cover', data.cover);
    formData.append('type_id', String(data.type_id));
    const response = await getClient().post<IEvent>('/events', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  async getEventTypes(params?: ITableParams) {
    const urlParams = new URLSearchParams();
    urlParams.append('page', String(params?.pagination?.page));
    urlParams.append('size', String(params?.pagination?.size));
    const response = await getClient().get<Array<IEventType>>(
      '/event-types?' + urlParams,
    );
    return response.data;
  },
  async voteEvent(data: IVoteEvent) {
    const response = await getClient().post(`/events/${data.eventId}/vote`, {
      like: data.like,
    });
    return response.data;
  },

  async deleteEvent(id: number) {
    const response = await getClient().delete(`/events/${id}`);
    return response.data;
  },

  async changeEventStatus(id: number, status: EventStatusEnum) {
    const response = await getClient().patch(`/events/${id}`, {
      status,
    });
    return response.data;
  },

  async getEventImage(uri: string) {
    const response = await getClient().get(uri, { responseType: 'blob' });
    return response.data;
  },
};
