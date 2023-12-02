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
}

export enum EventStatusEnum {
  OnReview = 'on_review',
  Rejected = 'rejected',
  OnPoll = 'on_poll',
  Planned = 'planned',
  Cancelled = 'cancelled',
  Ended = 'ended',
}
