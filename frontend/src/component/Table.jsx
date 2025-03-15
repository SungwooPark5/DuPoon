import Table from "react-bootstrap/Table";

function TableComponent() {
  return (
    <>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th rowSpan="2">연도</th>
            <th colSpan="4">투자</th>
          </tr>
          <tr>
            <th>수익</th>
            <th>입출금</th>
            <th>기말자산</th>
            <th>수익률</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>2021</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
          </tr>
          <tr>
            <td>2022</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
          </tr>
        </tbody>
      </Table>
    </>
  );
}

export default TableComponent;
