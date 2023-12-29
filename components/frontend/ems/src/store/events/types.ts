import { EventStatusEnum } from 'services/api/events/eventsApi.type';

export type EventType = {
  id: number;
  title: string;
  cover: {
    id: number;
    uri: string;
  } | null;
  status: EventStatusEnum;
  place: string;
  date: Date;
  votedYes: number;
  votedNo: number;
  version: number;
  description: string;
  userVote: boolean;
};
