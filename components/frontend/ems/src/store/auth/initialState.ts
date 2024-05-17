const authInitialState = {
  fetchStatus: {
    isLoading: false,
    error: '',
  },
  isAuth: false,
  isInit: false,
  role: null as null | string,
};

export default authInitialState;
