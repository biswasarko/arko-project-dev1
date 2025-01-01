import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import axios from 'axios';

export default function TransactionsTable() {
    const [transactions, setTransactions] = useState([]);

    const fetchTransactions = async () => {
        const response = await axios.get('http://127.0.0.1:5000/transactions');
        setTransactions(response.data);
    };

    useEffect(() => {
        fetchTransactions();
    }, []);

    return (
        <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell>Expense</TableCell>
                        <TableCell>Item</TableCell>
                        <TableCell>Category</TableCell>
                        <TableCell>SubCategory</TableCell>
                        <TableCell>Payment_Method</TableCell>
                        <TableCell>Essential_Flag</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {transactions.map((row, index) => (
                        <TableRow key={index}>
                            <TableCell>{row.Date}</TableCell>
                            <TableCell>{row.Expense}</TableCell>
                            <TableCell>{row.Item}</TableCell>
                            <TableCell>{row.SubCategory}</TableCell>
                            <TableCell>{row.Category}</TableCell>
                            <TableCell>{row.Payment_Method}</TableCell>
                            <TableCell>{row.Essential_Flag}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
