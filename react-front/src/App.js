import { useTable, useSortBy } from "react-table";
import useTickerToTable from "./hooks/useTickerToTable";
import Table from "./components/Table";
import logo from "./assets/logo.png";
import styled from "styled-components/macro";

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
    <>
      <ContainerWrapper>
        <StyledImg src={logo} alt="logo" />
      </ContainerWrapper>

      <Table
        getTableProps={getTableProps}
        getTableBodyProps={getTableBodyProps}
        headerGroups={headerGroups}
        rows={rows}
        prepareRow={prepareRow}
      />
    </>
  );
}

export default App;

const StyledImg = styled.img`
  border-radius: 50%;
  width: 64px;
  margin: 50px;
`;
const ContainerWrapper = styled.div`
  display: flex;
  justify-content: center;
`;
