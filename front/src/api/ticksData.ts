import HTTP from './HttpProvider';

export function getBestTicksData() {
  return HTTP.get('/get-basic-data');
}
