import { IOption } from 'shared/types/types';

export type CreateEventModalContainerProps = {
  open: boolean;
  onClose: () => void;
};

export interface ICreateEventField {
  title: string;
  description: string;
  cover: File;
  placeId: IOption;
  datetime: Date;
  dateend: Date;
  time: Date;
  typeId: IOption;
}
