import { useState } from "react";
import Table from "react-bootstrap/Table";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import TableComponent from "./Table";

function App() {
  // const [count, setCount] = useState(0);

  const [data, setData] = useState([
    {
      year: 2021,
      total: { profit: 0, deposit: 0, final_asset: 0, rate: 0 },
      investment: { profit: 0, deposit: 0, final_asset: 0, rate: 0 },
    },
  ]);

  const headers = [
    [
      {
        rowSpan: 2,
        colSpan: 1,
        name: "연도",
      },
      {
        rowSpan: 1,
        colSpan: 4,
        name: "전체",
      },
      {
        rowSpan: 1,
        colSpan: 4,
        name: "투자",
      },
    ],
    [
      {
        rowSpan: 1,
        colSpan: 1,
        name: "수익",
      },
      {
        rowSpan: 1,
        colSpan: 1,
        name: "입출금",
      },
      {
        rowSpan: 1,
        colSpan: 1,
        name: "기말자산",
      },
      {
        rowSpan: 1,
        colSpan: 1,
        name: "수익률",
      },
      {
        rowSpan: 1,
        colSpan: 1,
        name: "수익",
      },
      {
        rowSpan: 1,
        colSpan: 1,
        name: "입출금",
      },
      {
        rowSpan: 1,
        colSpan: 1,
        name: "기말자산",
      },
      {
        rowSpan: 1,
        colSpan: 1,
        name: "수익률",
      },
    ],
  ];

  return (
    <>
      <Container>
        <Row className="text-center m-3">
          <h1>두푼</h1>
        </Row>
        <TableComponent headers={headers} data={data} />
      </Container>
    </>
  );
}

export default App;
