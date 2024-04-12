import { getClient } from 'services/api/axios';
import type { ISection } from 'services/api/sections/sectionsApi.type';

export const SectionsApi = {
  async getAllSections() {
    const response = await getClient().get<Array<ISection>>('/clubs');
    return response.data;
  },

  async postSection(data: Omit<ISection, 'id'>) {
    const response = await getClient().post<ISection>('/clubs', data);
    return response.data;
  },

  async deleteSection(id: number) {
    const response = await getClient().delete(`/clubs/${id}`);
    return response.data;
  },

  async updateSection(event: ISection) {
    const response = await getClient().put('/clubs', event);
    return response.data;
  },
};
