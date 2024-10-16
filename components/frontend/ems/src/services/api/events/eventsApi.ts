import { getClient } from 'services/api/axios';
import {
  EventStatusEnum,
  ICheckFree,
  IEvent,
  IEventType,
  IPlace,
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
    formData.append('datetime', data.datetime);
    formData.append('description', data.description);
    formData.append('cover', data.cover);
    formData.append('dateend', data.dateend);
    formData.append('place_id', String(data.place_id));
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
  async getEventPlaces(params?: ITableParams) {
    const urlParams = new URLSearchParams();
    urlParams.append('page', String(params?.pagination?.page));
    urlParams.append('size', String(params?.pagination?.size));
    const response = await getClient().get<Array<IPlace>>(
      '/places?' + urlParams,
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

  async updateEvent(event: IEvent) {
    const response = await getClient().put('/events', event);
    return response.data;
  },

  async getEventImage(uri: string) {
    const response = await getClient().get(uri, { responseType: 'blob' });
    return response.data;
  },

  async checkIfPlaceFree(data: ICheckFree) {
    const params = new URLSearchParams();
    params.append('place_id', String(data.place_id));
    params.append('dateend', String(data.dateend));
    params.append('datestart', String(data.datetime));
    const response = await getClient().post<boolean>(
      '/events/check_date?' + params,
    );
    return response.data;
  },
};
