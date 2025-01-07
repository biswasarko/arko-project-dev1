import React, {useEffect, useState} from "react";
import axios from "axios";
import { BarChart } from '@mui/x-charts/BarChart';
import {Box, Button, FormControl, InputLabel, MenuItem, Select, Stack, TextField, Typography} from "@mui/material";

const uData = [4000, 3000, 2000, 2780, 1890, 2390, 3490];
const pData = [2400, 1398, 9800, 3908, 4800, 3800, 4300];
const xLabels = [
    'Page A',
    'Page B',
    'Page C',
    'Page D',
    'Page E',
    'Page F',
    'Page G',
];

export default function CatExpenseBarChart() {
    const [StartDt, setStartDt] = useState("");
    const [EndDt, setEndDt] = useState("");
    const [Category, setCategory] = useState("");
    const [formData, setFormData] = useState({});
    const [categoriesData, setCategoriesData] = useState({});
    const [selectedCategory, setSelectedCategory] = useState("");
    const [subcategories, setSubcategories] = useState({});
    const [selectedSubCategory, setSelectedSubCategory] = useState("");
    const [totalExpense, setTotalExpense] = useState(0);

    const [labels, setLabels] = useState([]);
    const [expense, setExpense] = useState([]);


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

    const handleChange = (e) => {
            const {name, value} = e.target;
            setFormData({
                ...formData,
                [name]: value
            });


        };

    const handleCategoryChange = (e) => {
        const category = e.target.value;
        setSelectedCategory(category);
        // Populate subcategories with all keys of the selected category
        setSubcategories(category ? Object.keys(categoriesData[category]) : []);
        // setIsEssential("")
    };

    const handleSubCategoryChange = (e) => {
        const subcategory = e.target.value;
        setSelectedSubCategory(subcategory);
        // Populate subcategories with all keys of the selected category
        // setSubcategories(category ? Object.keys(categoriesData[category]) : []);
        // setIsEssential("")
    };

    const handleSubmit = async (e) => {
        // const {name, value} = e.target;
        // setFormData({
        //     ...formData,
        //     [name]: value
        // });
        e.preventDefault();
        const data = {
            ...formData,
            Category: selectedCategory,
        }
        console.log(data);

        const response = await axios.post('http://127.0.0.1:5000/expenseDashboard', data);
        console.log(response.data.exp_df);
        console.log(response.data.exp_df.Expense);
        setTotalExpense(response.data.tot_exp)
        setLabels(response.data.exp_df.Date);
        setExpense(response.data.exp_df.Expense);

    };
    return (
        <Box sx={{ p: 4 }}>
        <Box component="form"  onSubmit={handleSubmit}>
            <Stack direction="row" spacing={1}>
                <Typography variant="inherit">Start Date</Typography>
                <TextField  name="Date_Start" type="date" value={formData.Date_Start}
                           onChange={handleChange}/>
                <Typography variant="inherit">End Date</Typography>
                <TextField  name="Date_End" type="date" value={formData.Date_End}
                           onChange={handleChange}/>
            </Stack>
            <Stack direction="row" spacing={1}>
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
                <Button type="submit" variant="contained" color="primary">Submit</Button>
            </Stack>
        </Box>
            {totalExpense.length > 0 && (
                <Box sx={{ mt: 4 }}>
                    <Typography variant="h5" component="p">Total: {totalExpense}</Typography>
                    <BarChart
                        width={500}
                        height={300}
                        series={[
                            {data: expense, label: 'expense', id: 'expense'},
                        ]}
                        xAxis={[{data: labels, scaleType: 'band'}]}
                    />
                </Box>

            )}


        </Box>

    );
    }
