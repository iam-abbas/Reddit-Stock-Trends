export default function Table({
  getTableProps,
  getTableBodyProps,
  headerGroups,
  rows,
  prepareRow,
}) {
  return (
    <table {...getTableProps()}>
      <thead>
        {headerGroups.map((headerGroup) => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map((column) => (
              <th
                {...column.getHeaderProps(column.getSortByToggleProps())}
                style={{
                  borderBottom: "solid 1px white",
                  background: "none",
                  color: "white",
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
                      color: "white",
                      padding: "10px",
                      textAlign: "center",
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
