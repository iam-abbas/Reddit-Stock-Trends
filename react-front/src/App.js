import { useMemo, useEffect, useState } from "react";
import { useTable, useSortBy } from "react-table";
function App() {
  const [apiData, setApiData] = useState([]);

  useEffect(() => {
    fetch("/get-basic-data")
      .then((res) => res.json())
      .then((data) => setApiData(data.data));
  }, []);

  const data = useMemo(
    () =>
      apiData.map((tickerData) => {
        return { ...tickerData };
      }),
    [apiData]
  );

  const columns = useMemo(
    () => [
      {
        Header: "Ticker",

        accessor: "Ticker", // accessor is the "key" in the data
      },

      {
        Header: "Mentions",

        accessor: "Mentions",
      },
      {
        Header: "Name",

        accessor: "Name",
      },
      {
        Header: "Industry",

        accessor: "Industry",
      },
      {
        Header: "	Previous Close",

        accessor: "PreviousClose",
      },
      {
        Header: "5d Low",

        accessor: "Low5d",
      },
      {
        Header: "5d High",

        accessor: "High5d",
      },
      {
        Header: "1d Change",

        accessor: "ChangePercent1d",
      },
      {
        Header: "5d Change",

        accessor: "ChangePercent5d",
      },
      {
        Header: "1mo Change",

        accessor: "ChangePercent1mo",
      },
    ],

    []
  );

  const {
    getTableProps,

    getTableBodyProps,

    headerGroups,

    rows,

    prepareRow,
  } = useTable({ columns, data }, useSortBy);

  return (
    <table {...getTableProps()} style={{ border: "solid 1px blue" }}>
      <thead>
        {headerGroups.map((headerGroup) => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map((column) => (
              <th
                {...column.getHeaderProps(column.getSortByToggleProps())}
                style={{
                  borderBottom: "solid 3px red",

                  background: "aliceblue",

                  color: "black",

                  fontWeight: "bold",
                }}
              >
                {column.render("Header")}
                <span>
                  {column.isSorted ? (column.isSortedDesc ? " 🔽" : " 🔼") : ""}
                </span>
              </th>
            ))}
          </tr>
        ))}
      </thead>

      <tbody {...getTableBodyProps()}>
        {rows.map((row) => {
          prepareRow(row);

          return (
            <tr {...row.getRowProps()}>
              {row.cells.map((cell) => {
                return (
                  <td
                    {...cell.getCellProps()}
                    style={{
                      padding: "10px",

                      border: "solid 1px gray",

                      background: "papayawhip",
                    }}
                  >
                    {cell.column.Header === "Ticker" ? (
                      <a
                        href={`https://tradingview.com/symbols/${cell.value}`}
                        target="_blank"
                      >
                        {cell.render("Cell")}
                      </a>
                    ) : (
                      cell.render("Cell")
                    )}
                  </td>
                );
              })}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export default App;
