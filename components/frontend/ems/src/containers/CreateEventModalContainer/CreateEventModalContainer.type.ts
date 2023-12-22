export type CreateEventModalContainerProps = {
  open: boolean;
  onClose: () => void;
};

export interface ICreateEventField {
  title: string;
  description: string;
  cover: File;
  place: string;
  datetime: Date;
  typeId: number;
}
