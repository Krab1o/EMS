import { createAsyncThunk } from '@reduxjs/toolkit';
import { SectionsApi } from 'services/api/sections/sectionsApi';
import { getSectionsAdapter } from './adapters';
import type { ISection } from 'services/api/sections/sectionsApi.type';

const getAllSections = createAsyncThunk('sections/getAllSections', async () => {
  const response = await SectionsApi.getAllSections();
  return getSectionsAdapter(response);
});

const postSection = createAsyncThunk(
  'sections/postSection',
  async (data: Omit<ISection, 'id'>, { dispatch }) => {
    await SectionsApi.postSection(data);
    dispatch(getAllSections());
  },
);

const deleteSection = createAsyncThunk(
  'events/deleteEvent',
  async (id: number, { dispatch }) => {
    await SectionsApi.deleteSection(id);
    dispatch(getAllSections());
  },
);

const updateSection = createAsyncThunk(
  'events/updateEvent',
  async (data: ISection, { dispatch }) => {
    await SectionsApi.updateSection(data);
    dispatch(getAllSections());
  },
);

export { deleteSection, getAllSections, postSection, updateSection };
