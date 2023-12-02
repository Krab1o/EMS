import { IEvent } from 'services/api/api.type';
import { EventType } from './types';

function getEventsAdapter(data: Array<IEvent>): Array<EventType> {
  return data.map((event) => {
    return {
      id: event.id,
      title: event.title,
      cover: event.cover,
      status: event.status,
      place: event.place,
      date: new Date(event.datetime),
      votedYes: event.voted_yes,
      votedNo: event.voted_no,
      version: event.version,
      description: event.description,
    };
  }) as Array<EventType>;
}

export { getEventsAdapter };
