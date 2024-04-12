import sectionsInitialState from './initialState';
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { getAllSections } from './requests';
import type { SectionType } from './types';

const sectionsSlice = createSlice({
  name: 'sections',
  initialState: sectionsInitialState,
  reducers: {
    setCurrentSection: (state, action: PayloadAction<SectionType>) => {
      state.currentSection = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(getAllSections.fulfilled, (state, action) => {
      state.sections = action.payload;
    });
  },
});

export default sectionsSlice;
