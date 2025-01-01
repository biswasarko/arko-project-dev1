import React from 'react';
import {AppBar, IconButton, Toolbar, Typography} from "@mui/material";
import MenuIcon from '@mui/icons-material/Menu';

function Appheader() {
    return ( <AppBar position="static">
        <Toolbar>
            <IconButton onClick={() => console.log('Menu button clicked')} color="secondary">
                <MenuIcon />
            </IconButton>
            <Typography variant="h6" gutterBottom variant="h6">Expense Form</Typography>
        </Toolbar>
    </AppBar>);
}

/** @type {import("@mui/material").SxProps} */
const styles = {
    appBar: {
        bgcolor: 'neutral.main'
    }
}

export default Appheader;