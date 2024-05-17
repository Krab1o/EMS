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
  dateEnd: Date;
  votedYes: number;
  votedNo: number;
  version: number;
  description: string;
  userVote: boolean;
};

export type PlaceType = {
  id: number;
  title: string;
  floor: number;
  institutionId: number;
  institution: IInstitution;
};
