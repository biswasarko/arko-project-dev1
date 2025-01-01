import React, { useState, useEffect } from 'react';
import {
    TextField,
    Button,
    Select,
    MenuItem,
    FormControl,
    InputLabel,
    Switch,
    FormControlLabel,
    Container, Grid, Stack
} from '@mui/material';
import axios from 'axios';
import Grid2 from "@mui/material/Unstable_Grid2";

const subCategoryOptions = ["Cigarette", "Alcohol", "Lighter"]; // Add more

export default function ExpenseForm({ refreshData }) {
    const [formData, setFormData] = useState({
        Date: "",
        Expense: "",
        Item: "",
        Category: "",
        Payment_Method: "",
        Essential_Flag: "",
    });
    const [categoriesData, setCategoriesData] = useState({});
    const [selectedCategory, setSelectedCategory] = useState("");
    const [subcategories, setSubcategories] = useState([]);
    const [selectedSubCategory, setSelectedSubCategory] = useState("");
    const [isEssential, setIsEssential] = useState("");
    const [selectedPaymentMethod, setSelectedPaymentMethod] = useState("");

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData({
            ...formData,
            [name]: type === "checkbox" ? checked : value,
        });
        console.log("inside handle change");
    };

    const handleSubmit = async (event) => {
        // event.preventDefault();
        console.log("inside submit");
        console.log(formData);
        const data = {
            ...formData,
            Category: selectedCategory,
            SubCategory: selectedSubCategory,
            Essential_Flag: isEssential,
            Payment_Method: selectedPaymentMethod,
        }

        setFormData(data);

        console.log(data);
        await axios.post('http://127.0.0.1:5000/submit', data);
        refreshData();
    };

    // Fetch JSON data
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const response = await fetch("/category_mapping.json");
                if (!response.ok) {
                    throw new Error("Failed to fetch categories");
                }
                const data = await response.json();
                setCategoriesData(data);
            } catch (error) {
                console.error("Error fetching categories:", error);
            }
        };

        fetchCategories();
    }, []);

    const handleCategoryChange = (e) => {
        const category = e.target.value;
        setSelectedCategory(category);
        // Populate subcategories with all keys of the selected category
        setSubcategories(category ? Object.keys(categoriesData[category]) : []);
        setIsEssential("")
    };

    const handleSubCategoryChange = (e) => {
        const subCategory = e.target.value;

        setSelectedSubCategory(subCategory);
        setIsEssential(categoriesData[selectedCategory][subCategory]);


    }

    const handlePaymentMethodChange = (e) => {
        const paymentMethod = e.target.value;

        setSelectedPaymentMethod(paymentMethod);
    }

    return (

            <form onSubmit={handleSubmit}>
                <Stack direction='column' spacing={5}>
                    <TextField label="Date" name="Date" type="date" value={formData.Date} onChange={handleChange}  />
                    <TextField label="Expense" name="Expense" value={formData.Expense} onChange={handleChange}  />
                    <TextField label="Item" name="Item" value={formData.Item} onChange={handleChange}  />
                    {/* Category Dropdown */}
                    <FormControl fullWidth sx={{marginBottom: 2}}>
                        <InputLabel id="category-label">Category</InputLabel>
                        <Select
                            labelId="category-label"
                            id="category"
                            value={selectedCategory}
                            onChange={handleCategoryChange}
                            label="Category"
                        >
                            <MenuItem value="">
                                <em>--Select Category--</em>
                            </MenuItem>
                            {Object.keys(categoriesData).map((category) => (
                                <MenuItem key={category} value={category}>
                                    {category}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    {/* Subcategory Dropdown */}
                    <FormControl fullWidth disabled={!selectedCategory}>
                        <InputLabel id="subcategory-label">Subcategory</InputLabel>
                        <Select
                            labelId="subcategory-label"
                            id="subcategory"
                            value={selectedSubCategory}
                            onChange={handleSubCategoryChange}
                            label="Subcategory"
                        >
                            <MenuItem value="">
                                <em>--Select Subcategory--</em>
                            </MenuItem>
                            {subcategories.map((subcategory) => (
                                <MenuItem key={subcategory} value={subcategory}>
                                    {subcategory}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <TextField label="Essential Flag" name="Essential_Flag" value={isEssential} disabled/>
                    <Select
                        labelId="payment-label"
                        id="Payment_Method"
                        value={selectedPaymentMethod}
                        label="Payment Method"
                        onChange={handlePaymentMethodChange}
                        >
                        <MenuItem value="">
                            <em>--Select Payment Mode--</em>
                        </MenuItem>
                        <MenuItem value="UPI">UPI</MenuItem>
                        <MenuItem value="CC">Credit Card</MenuItem>
                        <MenuItem value="CASH">Cash</MenuItem>
                        <MenuItem value="AT">Account Transfer</MenuItem>
                        <MenuItem value="Fastag">Fastag</MenuItem>
                    </Select>
                    {/*<TextField label="Payment Method" name="Payment_Method" value={formData.Payment_Method} onChange={handleChange} />*/}
                    <Button type="submit" variant="contained" color="primary">Submit</Button>
                </Stack>
            </form>
    );
}
