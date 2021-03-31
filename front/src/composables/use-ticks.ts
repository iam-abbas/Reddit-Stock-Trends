import { reactive, computed } from 'vue';
import { getBestTicksData } from '@/api/ticksData';

interface TickData {
  Ticker: string;
  Mentions: number;
  Name: string;
  Industry: string;
  PreviousClose: number;
  Low5d: number;
  High5d: number;
  ChangePercent1d: number;
  ChangePercent5d: number;
  ChangePercent1mo: number;
}

interface State {
  list: TickData[];
}

export function useArtists() {
  const state: State = reactive({
    list: [],
    listLength: computed(() => state.list.length),
  });

  async function get(page: number) {
    const tempData: [] = (await getBestTicksData(page)).data;
    state.list = [];

    tempData.forEach((elem: any) => {
      const tickData: TickData = {
        Ticker: elem.Ticker,
        Mentions: elem.Mentions,
        Name: elem.Name,
        Industry: elem.Industry,
        PreviousClose: elem.PreviousClose,
        Low5d: elem.Low5d,
        High5d: elem.High5d,
        ChangePercent1d: elem.ChangePercent1d,
        ChangePercent5d: elem.ChangePercent5d,
        ChangePercent1mo: elem.ChangePercent1mo,
      };

      state.list.push(tickData);
    });
  }

  return {
    state,
    get,
  };
}
