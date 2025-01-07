import React, {useState, useMemo, useEffect} from "react";
import { Line } from "react-chartjs-2";
import {
    Box,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
} from "@mui/material";
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
} from "chart.js";
import axios from "axios";

// Register Chart.js components
ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

// Data






const Dashboard = () => {
    // States for filters
    const [selectedCategory, setSelectedCategory] = useState("");
    const [selectedSubCategory, setSelectedSubCategory] = useState("");
    const [selectedDate, setSelectedDate] = useState("");
    const [data, setData] = useState({});

    useEffect(() => {
        const fetchExpenseData = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/expenseDashboard");
                const data = response.data;
                setData(data);
                console.log(data);
            } catch (error) {
                console.error("Error fetching form schema:", error);
            }
        };
        fetchExpenseData();
    },[]);

    // Parse raw data
    const parseData = (data) => {
        const result = [];
        for (const key in data) {
            const match = key.match(
                /\('([^']*)', '([^']*)', '([^']*)'\)/ // Regex to parse the key
            );
            if (match) {
                const [_, date, category, subCategory] = match;
                result.push({
                    date,
                    category,
                    subCategory,
                    value: data[key],
                });
            }
        }
        return result;
    };

    const parsedData = parseData(data.Expense);

    // Extract unique values for filters
    const categories = useMemo(
        () => [...new Set(parsedData.map((item) => item.category))],
        []
    );

    const subCategories = useMemo(() => {
        return selectedCategory
            ? [
                ...new Set(
                    parsedData
                        .filter((item) => item.category === selectedCategory)
                        .map((item) => item.subCategory)
                ),
            ]
            : [];
    }, [selectedCategory]);

    const dates = useMemo(() => {
        return [...new Set(parsedData.map((item) => item.date))];
    }, []);

    // Filter data for the chart
    const filteredData = useMemo(() => {
        return parsedData.filter((item) => {
            const categoryMatch =
                !selectedCategory || item.category === selectedCategory;
            const subCategoryMatch =
                !selectedSubCategory || item.subCategory === selectedSubCategory;
            const dateMatch = !selectedDate || item.date === selectedDate;
            return categoryMatch && subCategoryMatch && dateMatch;
        });
    }, [selectedCategory, selectedSubCategory, selectedDate]);

    // Prepare chart data
    const chartData = useMemo(() => {
        const groupedData = {};
        filteredData.forEach((item) => {
            if (!groupedData[item.date]) {
                groupedData[item.date] = 0;
            }
            groupedData[item.date] += item.value;
        });

        const labels = Object.keys(groupedData).sort();
        const data = labels.map((date) => groupedData[date]);

        return {
            labels,
            datasets: [
                {
                    label: "Expenses",
                    data,
                    borderColor: "rgba(75,192,192,1)",
                    fill: false,
                },
            ],
        };
    }, [filteredData]);

    return (
        <Box>
            {/* Date Filter */}
            <FormControl fullWidth margin="normal">
                <InputLabel id="date-label">Select Date</InputLabel>
                <Select
                    labelId="date-label"
                    value={selectedDate}
                    onChange={(e) => setSelectedDate(e.target.value)}
                >
                    <MenuItem value="">All</MenuItem>
                    {dates.map((date) => (
                        <MenuItem key={date} value={date}>
                            {date}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>

            {/* Category Filter */}
            <FormControl fullWidth margin="normal">
                <InputLabel id="category-label">Select Category</InputLabel>
                <Select
                    labelId="category-label"
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                >
                    <MenuItem value="">All</MenuItem>
                    {categories.map((category) => (
                        <MenuItem key={category} value={category}>
                            {category}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>

            {/* Sub-Category Filter */}
            <FormControl fullWidth margin="normal">
                <InputLabel id="sub-category-label">Select Sub-Category</InputLabel>
                <Select
                    labelId="sub-category-label"
                    value={selectedSubCategory}
                    onChange={(e) => setSelectedSubCategory(e.target.value)}
                >
                    <MenuItem value="">All</MenuItem>
                    {subCategories.map((subCategory) => (
                        <MenuItem key={subCategory} value={subCategory}>
                            {subCategory}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>

            {/* Line Chart */}
            <Line data={chartData} />
        </Box>
    );
};

export default Dashboard;
