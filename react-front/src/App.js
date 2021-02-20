import { useTable, useSortBy } from "react-table";
import useTickerToTable from "./hooks/useTickerToTable";
import Table from "./components/Table";

function App() {
  const { data, columns } = useTickerToTable();
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({ columns, data }, useSortBy);

  return (
    <Table
      getTableProps={getTableProps}
      getTableBodyProps={getTableBodyProps}
      headerGroups={headerGroups}
      rows={rows}
      prepareRow={prepareRow}
    />
  );
}

export default App;
