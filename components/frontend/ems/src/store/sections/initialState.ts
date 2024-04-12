import type { SectionType } from './types';

const sectionsInitialState = {
  sections: null as null | Array<SectionType>,
  currentSection: null as null | SectionType,
};

export default sectionsInitialState;
