import type { SectionType } from './types';
import type { ISection } from 'services/api/sections/sectionsApi.type';

function getSectionsAdapter(data: Array<ISection>): Array<SectionType> {
  return data.map((event) => {
    return {
      id: event.id,
      title: event.title,
      description: event.description,
    };
  }) as Array<SectionType>;
}

export { getSectionsAdapter };
