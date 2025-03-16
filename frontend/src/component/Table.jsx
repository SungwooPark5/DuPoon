import Table from "react-bootstrap/Table";

function TableComponent({ headers, data }) {
  if (!headers) {
    throw new Error("headers is required");
  }

  return (
    <>
      <Table striped bordered hover>
        <thead>
          {headers.map((row, index) => (
            <tr>
              {row.map((header) => (
                <th
                  rowSpan={header.rowSpan}
                  colSpan={header.colSpan}
                  key={header.name}
                >
                  {header.name}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {data.map((row, index) => {
            return (
              <tr key={index}>
                <td>{row.year}</td>
                <td>{row.total.profit}</td>
                <td>{row.total.deposit}</td>
                <td>{row.total.final_asset}</td>
                <td>{row.total.rate}</td>
                <td>{row.investment.profit}</td>
                <td>{row.investment.deposit}</td>
                <td>{row.investment.final_asset}</td>
                <td>{row.investment.rate}</td>
              </tr>
            );
          })}
        </tbody>
      </Table>
    </>
  );
}

export default TableComponent;
