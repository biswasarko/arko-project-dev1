import {Container, Stack, Typography} from "@mui/material";
import Appheader from "./Appheader";
import ExpenseForm from "./ExpenseForm";
import TransactionsTable from "./TransactionsTable";
import React, {useState} from "react";

export default function HomePage() {
    return (
        <Container>
            <Stack direction='column' spacing={12}>
                <Typography variant='h4' component='h2'>Home</Typography>
            </Stack>
        </Container>
    );
}