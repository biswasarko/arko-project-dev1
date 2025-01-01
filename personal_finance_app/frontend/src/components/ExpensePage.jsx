import {Container, Stack} from "@mui/material";
import Appheader from "./Appheader";
import ExpenseForm from "./ExpenseForm";
import TransactionsTable from "./TransactionsTable";
import React, {useState} from "react";

export default function ExpensePage() {
    const [refresh, setRefresh] = useState(false);

    const refreshData = () => setRefresh(!refresh);

    return (
        <Container>
            <Stack direction='column' spacing={12}>
                <ExpenseForm refreshData={refreshData}/>
                <TransactionsTable key={refresh}/>
            </Stack>
        </Container>
    );
}