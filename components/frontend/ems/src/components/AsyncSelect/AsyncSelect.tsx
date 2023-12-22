import React, { useCallback, useMemo, useState } from 'react';
import debounce from 'shared/utils/debounce/debounce';
import { Select } from 'antd';
import type { IOption } from 'shared/types/types';
import type { AsyncSelectProps } from 'components/AsyncSelect/AsyncSelect.type';

export function AsyncSelect({
  fetchOptions,
  debounceTimeout = 500,
  ...props
}: AsyncSelectProps) {
  const [fetching, setFetching] = useState(false);
  const [options, setOptions] = useState<Array<IOption>>([]);
  const [isNextPage, setIsNextPage] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);

  const loadOptions = useCallback(
    (offset = 1) => {
      fetchOptions({
        pagination: {
          page: offset,
          size: 10,
        },
      }).then((data) => {
        setIsNextPage(true);

        const newOptions: Array<IOption> = data.map((item) => ({
          label: item.title,
          value: String(item.id),
          key: String(item.id),
        }));

        setOptions((prev) => [...prev, ...newOptions]);
        setFetching(false);
      });
    },
    [fetchOptions],
  );

  const debounceFetcher = useMemo(() => {
    setOptions([]);
    return debounce(loadOptions, debounceTimeout);
  }, [debounceTimeout, loadOptions]);

  function onScroll(e: React.UIEvent<HTMLDivElement, UIEvent>) {
    const elem = e.currentTarget;

    if (Math.abs(elem.scrollHeight - elem.scrollTop - elem.clientHeight) <= 5) {
      if (isNextPage) {
        setIsNextPage(false);
        const debounceLoad = debounce(loadOptions, debounceTimeout);
        setFetching(true);
        setCurrentPage((prev) => prev + 1);
        debounceLoad(currentPage + 1);
      }
    }
  }

  function dropSelect(isOpen: boolean) {
    if (isOpen) {
      setFetching(true);
      debounceFetcher();
    } else {
      setOptions([]);
      setCurrentPage(1);
      setIsNextPage(false);
    }
  }

  return (
    <Select
      onPopupScroll={onScroll}
      labelInValue
      filterOption={false}
      onDropdownVisibleChange={dropSelect}
      loading={fetching}
      notFoundContent={null}
      {...props}
      options={options}
    />
  );
}
