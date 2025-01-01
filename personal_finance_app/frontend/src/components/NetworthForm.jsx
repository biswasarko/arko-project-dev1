import React, {useEffect, useState} from "react";
import axios from "axios";
import {Box, Button, Grid, Stack, TextField, Typography} from "@mui/material";

export default function NetworthForm({ refreshData }) {
    const [formData, setFormData] = useState({});
    const [formSchema, setFormSchema] = useState({});

    useEffect(() => {
        console.log('inside useeffect');
        const fetchData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/get_headers');
                console.log("response");
                console.log(response);
                const data = response.data;
                console.log("data");
                console.log(data);
                setFormSchema(data);
            } catch (error) {
                console.error(error);
            }
        };
        fetchData();

    }, []);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const data = { ...formData };
        setFormData(data);
        // await axios.post('http://127.0.0.1:5000/networth_submit', data);
        // refreshData();
        console.log('after submit');
        // console.log({formSchema.map((field, index) => (index))});
    };

    return (
        <Box
            component="form"
            onSubmit={handleSubmit}
            sx={{ maxWidth: 600, mx: "auto", mt: 4 }}
        >
            <Typography variant="h4" gutterBottom>
                Dynamic Form
            </Typography>
            {/*<Typography component="h1" variant="h5" gutterBottom>*/}
            {/*    {formSchema.fields.map((field, i) => (*/}
            {/*        <TextField name={field.name} label={field.label} />*/}
            {/*    ))}*/}
            {/*</Typography>*/}
            {/*{formSchema.fields.map((field) => (*/}
            {/*    <Box key={field.name} sx={{ mb: 2 }}>*/}
            {/*        {field.type === "number" || field.type === "text" || field.type === "date" ? (*/}
            {/*            <TextField*/}
            {/*                fullWidth*/}
            {/*                label={field.label}*/}
            {/*                name={field.name}*/}
            {/*                type={field.type}*/}
            {/*                required={field.required === "true"}*/}
            {/*                defaultValue={field.defaultValue}*/}
            {/*                // onChange={handleInputChange}*/}
            {/*            />*/}
            {/*        ) : null}*/}
            {/*    </Box>*/}
            {/*))}*/}

            {/*<Grid container spacing={2}>*/}
            {/*    {formSchema?.fields.map((field, index) => (*/}
            {/*        index))};*/}
            {/*</Grid>*/}


            <Button type="submit" variant="contained" color="primary">
                Submit
            </Button>
        </Box>
    );
};