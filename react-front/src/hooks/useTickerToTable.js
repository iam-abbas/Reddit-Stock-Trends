import { useMemo, useEffect, useState } from "react";

export default function useTickerToTable() {
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

  return { data, columns };
}
