/// <reference types="react-scripts" />

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      REACT_APP_BASE_URL: string;
      REACT_APP_ENV: 'dev' | 'prod';
    }
  }
}

export {};
