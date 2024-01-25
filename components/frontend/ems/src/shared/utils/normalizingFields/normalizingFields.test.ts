import { normalize, deNormalize } from './normalizingFields';

const mockWithDate = {
  value1: '23',
  value2: 23,
  value3: undefined,
  date: new Date(2013, 3, 3, 3, 34, 14),
};

const mockWithDateString = {
  value1: '23',
  value2: 23,
  value3: undefined,
  date: '2013-04-02T23:34:14.000Z',
};

describe('normalizing', () => {
  test('Валидация объекта с датой', () => {
    expect(normalize(mockWithDate)).toEqual(mockWithDateString);
    expect(normalize(mockWithDate)).toMatchSnapshot();
  });
  test('Валидация объекта со строкой', () => {
    expect(deNormalize(mockWithDateString)).toEqual(mockWithDate);
    expect(deNormalize(mockWithDateString)).toMatchSnapshot();
  });
});
