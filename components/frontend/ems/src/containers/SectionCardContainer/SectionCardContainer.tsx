import { useNavigate } from 'react-router-dom';
import { useAppDispatch } from 'store';
import { SectionCard } from 'components/SectionCard/SectionCard';
import { deleteSection, sectionsActions } from 'store/sections';
import type { SectionCardContainerProps } from './SectionCardContainer.type';
import { useSelector } from 'react-redux';
import { selectRole } from 'store/auth';

export function SectionCardContainer({
  initialData,
}: SectionCardContainerProps) {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const role = useSelector(selectRole);

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
      role={role}
    />
  );
}
