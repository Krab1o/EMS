export type CreateSectionModalContainerProps = {
  open: boolean;
  onClose: () => void;
};

export interface ICreateSectionField {
  title: string;
  description: string;
  telegram: string;
  vk: string;
  youtube: string;
  rutube: string;
  tiktok: string;
}
