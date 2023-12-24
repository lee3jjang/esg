import { DataGrid, GridColDef, GridValueGetterParams } from "@mui/x-data-grid";

type TSampleDataGridProps = { className?: string };

export const SampleDataGrid = ({ className }: TSampleDataGridProps) => {
  const columns: GridColDef[] = [
    { field: "id", headerName: "아이디", width: 70 },
    { field: "firstName", headerName: "성", width: 130 },
    { field: "lastName", headerName: "이름", width: 130 },
    {
      field: "age",
      headerName: "나이",
      type: "number",
      width: 90,
    },
    {
      field: "fullName",
      headerName: "전체 이름",
      description: "전체 이름입니다.",
      sortable: false,
      width: 160,
      valueGetter: ({ row: { firstName, lastName } }: GridValueGetterParams) =>
        `${firstName || ""} ${lastName || ""}`,
    },
  ];

  const rows = [
    { id: 1, lastName: "Snow", firstName: "Jon", age: 35 },
    { id: 2, lastName: "Lannister", firstName: "Cersei", age: 42 },
    { id: 3, lastName: "Lannister", firstName: "Jaime", age: 45 },
    { id: 4, lastName: "Stark", firstName: "Arya", age: 16 },
    { id: 5, lastName: "Targaryen", firstName: "Daenerys", age: null },
    { id: 6, lastName: "Lee", firstName: "SangJin", age: 150 },
    { id: 7, lastName: "Clifford", firstName: "Ferrara", age: 44 },
    { id: 8, lastName: "Frances", firstName: "Rossini", age: 36 },
    { id: 9, lastName: "Roxie", firstName: "Harvey", age: 65 },
  ];

  return (
    <DataGrid
      className={className}
      rows={rows}
      columns={columns}
      initialState={{
        pagination: {
          paginationModel: { page: 0, pageSize: 5 },
        },
      }}
      pageSizeOptions={[5, 10]}
      checkboxSelection
    />
  );
};
