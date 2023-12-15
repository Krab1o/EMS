export type CreateEventModalContainerProps = {
  open: boolean;
  onClose: () => void;
};

export interface ICreateEventField {
  title: string;
  description: string;
  coverId: number | null;
  place: string;
  datetime: Date;
  typeId: number;
}
