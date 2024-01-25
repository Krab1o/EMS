import type { IModalState } from 'shared/types/types';

const appInitialState = {
  modalState: {
    isOpen: false,
    modalType: null,
    initialData: null,
    title: '',
  } as IModalState,
};

export default appInitialState;
