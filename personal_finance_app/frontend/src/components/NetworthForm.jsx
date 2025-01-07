import React, { useEffect, useState } from "react";
import axios from "axios";
import { Box, Button, Stack, TextField, Typography } from "@mui/material";

export default function NetworthForm({ refreshData }) {
    const [formData, setFormData] = useState({});
    const [formSchema, setFormSchema] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/get_headers");
                const data = response.data;
                setFormSchema(data);


                const initialFormData = {};
                data.fields.forEach((field) => {
                    if (field.type === "date") {
                        // Set default value for date fields to today's date
                        initialFormData[field.name] = new Date().toISOString().split("T")[0];
                    } else {
                        initialFormData[field.name] = field.defaultValue;
                    }
                });
                setFormData(initialFormData);
            } catch (error) {
                console.error("Error fetching form schema:", error);
            }
        };
        fetchData();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        console.log(name, value);
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = { ...formData };
            console.log("Submitting Data:", data);
            await axios.post("http://127.0.0.1:5000/networthSubmit", data);
            if (refreshData) refreshData();
        } catch (error) {
            console.error("Error submitting form:", error);
        }
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
            <Stack spacing={5}>
                {formSchema && formSchema.fields ? (
                    formSchema.fields.map((field, index) => (
                        <Stack key={index} spacing={1}>
                            <Typography variant="caption">{field.label}</Typography>
                            <TextField
                                id={field.name}
                                name={field.name}
                                type={field.type}
                                value={formData[field.name] || ""}
                                onChange={handleChange}
                            />
                        </Stack>
                    ))
                ) : (
                    <Typography>Form schema not available</Typography>
                )}
            </Stack>
            <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
                Submit
            </Button>
        </Box>
    );
}
