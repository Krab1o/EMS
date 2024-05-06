export interface IEvent {
  id: number;
  title: string;
  cover: {
    id: number;
    uri: string;
  } | null;
  status: EventStatusEnum;
  place?: IPlace;
  datetime: string;
  voted_yes: number;
  voted_no: number;
  version: number;
  description: string;
  user_vote: boolean;
}

export interface IPlace {
  id: 0;
  title: string;
  floor: 0;
  institution_id: 0;
  institution: IInstitution;
}

export interface IInstitution {
  id: 0;
  title: string;
  description: string;
  version: 0;
}

export interface IEventType {
  id: number;
  title: string;
  description: string;
}

export enum EventStatusEnum {
  OnReview = 'on_review',
  Rejected = 'rejected',
  OnPoll = 'on_poll',
  Planned = 'planned',
  Cancelled = 'cancelled',
  Ended = 'ended',
}

export interface IPostEvent {
  title: string;
  description: string;
  cover: File;
  place: string;
  datetime: string;
  type_id: number;
}

export interface IVoteEvent {
  eventId: number;
  like: boolean;
}
