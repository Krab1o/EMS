import '@testing-library/jest-dom/extend-expect';
import { fireEvent, render, screen } from '@testing-library/react';
import Login from './Login';
import userEvent from '@testing-library/user-event';

describe('Login component', () => {
  let submitFn: jest.Mock;
  beforeEach(() => {
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: jest.fn().mockImplementation((query) => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(), // Deprecated
        removeListener: jest.fn(), // Deprecated
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
      })),
    });
    submitFn = jest.fn();
  });
  test('Субмит формы логина', async () => {
    render(
      <Login
        postLogin={submitFn}
        fetchStatus={{ error: '', isLoading: false }}
      />,
    );

    screen.getByTestId('loginForm').onsubmit = submitFn;
    fireEvent.change(screen.getByTestId('loginInput'), {
      target: { value: 'Vasya' },
    });
    fireEvent.change(screen.getByTestId('passInput'), {
      target: { value: 'qwerty' },
    });
    expect(screen.getByTestId('loginInput')).toHaveValue('Vasya');
    expect(screen.getByTestId('passInput')).toHaveValue('qwerty');

    userEvent.type(screen.getByTestId('loginInput'), '123');
    expect(screen.getByTestId('loginInput')).toHaveValue('Vasya123');

    fireEvent.click(screen.getByTestId('loginBtn'));
    expect(submitFn).toHaveBeenCalled();
  });
  test('Отображение ошибки формы логина', () => {
    render(
      <Login
        postLogin={submitFn}
        fetchStatus={{ error: 'SomeError', isLoading: false }}
      />,
    );
    expect(screen.getByTestId('loginError')).toBeInTheDocument();
  });
});
