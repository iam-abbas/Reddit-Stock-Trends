import HTTP from './HttpProvider';

export function getBestTicksData(page: number) {
  return HTTP.get(`/get-basic-data?page=${page}`);
}
