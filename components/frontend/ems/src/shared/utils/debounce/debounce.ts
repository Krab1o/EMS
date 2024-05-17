export default function debounce(
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  loadData: (...args: any) => void,
  debounceTimeout: number,
) {
  let timeOut: NodeJS.Timeout | null = null;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  return (...args: any) => {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    // eslint-disable-next-line @typescript-eslint/no-this-alias,@typescript-eslint/ban-ts-comment
    const context = this;
    if (timeOut) clearTimeout(timeOut);
    timeOut = setTimeout(() => {
      loadData.apply(context, args);
      timeOut = null;
    }, debounceTimeout);
  };
}
