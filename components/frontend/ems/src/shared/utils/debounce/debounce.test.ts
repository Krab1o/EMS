import debounce from './debounce';
jest.useFakeTimers();

describe('debounce', () => {
  let func: jest.Mock;
  let debouncedFunc: () => void;

  beforeEach(() => {
    func = jest.fn();
    debouncedFunc = debounce(func, 1000);
  });

  test('ИСполнение лишь один раз', () => {
    for (let i = 0; i < 1000; i++) {
      debouncedFunc();
    }

    jest.runAllTimers();

    expect(func).toBeCalledTimes(1);
  });
});
