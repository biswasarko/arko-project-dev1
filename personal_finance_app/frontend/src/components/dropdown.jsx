import React, { useState, useEffect } from "react";
import { Box, FormControl, InputLabel, Select, MenuItem } from "@mui/material";

const Dropdowns = () => {
    const [categoriesData, setCategoriesData] = useState({});
    const [selectedCategory, setSelectedCategory] = useState("");
    const [subcategories, setSubcategories] = useState([]);

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
    };

    return (
        <Box sx={{ minWidth: 300, padding: 2 }}>
            {/* Category Dropdown */}
            <FormControl fullWidth sx={{ marginBottom: 2 }}>
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
                    value=""
                    onChange={() => {}} // Optional: Add logic if needed
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
        </Box>
    );
};

export default Dropdowns;
