import { useNavigate } from 'react-router-dom';
import { useAppDispatch } from 'store';
import { SectionCard } from 'components/SectionCard/SectionCard';
import { deleteSection, sectionsActions } from 'store/sections';
import type { SectionCardContainerProps } from './SectionCardContainer.type';

export function SectionCardContainer({
  initialData,
}: SectionCardContainerProps) {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const onCardClick = () => {
    dispatch(sectionsActions.setCurrentSection(initialData));
    navigate(`${initialData.id}`);
  };

  const onDelete = () => {
    dispatch(deleteSection(initialData.id));
  };

  return (
    <SectionCard
      initialData={initialData}
      onCardClick={onCardClick}
      onDelete={onDelete}
    />
  );
}
