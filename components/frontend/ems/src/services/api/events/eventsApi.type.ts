export interface IEvent {
  id: number;
  title: string;
  cover: string;
  status: EventStatusEnum;
  place: string;
  datetime: string;
  voted_yes: number;
  voted_no: number;
  version: number;
  description: string;
  user_vote: boolean;
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
