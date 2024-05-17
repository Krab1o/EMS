import type { EventType } from './types';
import type { IEvent } from 'services/api/events/eventsApi.type';

function getEventsAdapter(data: Array<IEvent>): Array<EventType> {
  return data.map((event) => {
    return {
      id: event.id,
      title: event.title,
      cover: event.cover,
      status: event.status,
      place: { ...event.place, institutionId: event.place?.institution_id },
      date: new Date(event.datetime),
      votedYes: event.voted_yes,
      votedNo: event.voted_no,
      version: event.version,
      description: event.description,
      userVote: event.user_vote,
      dateEnd: new Date(event.dateend),
    };
  }) as Array<EventType>;
}

export { getEventsAdapter };
