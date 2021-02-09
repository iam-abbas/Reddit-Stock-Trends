import { reactive, computed } from 'vue';
import { getBestTicksData } from '@/api/ticksData';

interface State {
  list: [];
}

export function useArtists() {
  const state: State = reactive({
    list: [],
    listLength: computed(() => state.list.length),
  });

  async function get() {
    state.list = (await getBestTicksData()).data;
  }

  return {
    state,
    get,
  };
}
