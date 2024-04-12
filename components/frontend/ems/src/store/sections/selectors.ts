import { RootState } from 'store';

function selectSections(state: RootState) {
  return state.sections.sections;
}

function selectCurrentSection(state: RootState) {
  return state.sections.currentSection;
}

export { selectSections, selectCurrentSection };
