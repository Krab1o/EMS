import {
  EventStatusEnum,
  IInstitution,
} from 'services/api/events/eventsApi.type';

export type EventType = {
  id: number;
  title: string;
  cover: {
    id: number;
    uri: string;
  } | null;
  status: EventStatusEnum;
  place: PlaceType;
  date: Date;
  votedYes: number;
  votedNo: number;
  version: number;
  description: string;
  userVote: boolean;
};

export type PlaceType = {
  id: 0;
  title: string;
  floor: 0;
  institutionId: 0;
  institution: IInstitution;
};
