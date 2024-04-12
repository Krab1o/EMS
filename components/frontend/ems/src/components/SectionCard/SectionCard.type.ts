import type { SectionType } from 'store/sections/types';

export type SectionCardProps = {
  initialData: SectionType;
  onCardClick: () => void;
  onDelete: () => void;
};
