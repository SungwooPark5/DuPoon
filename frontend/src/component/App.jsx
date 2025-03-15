import { useState } from "react";
import Table from "react-bootstrap/Table";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import TableComponent from "./Table";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <Container>
        <h1>두푼</h1>
        <TableComponent />
      </Container>
    </>
  );
}

export default App;
