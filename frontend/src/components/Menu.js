import React from 'react';
import {render} from "react-dom";

import Paper from "@material-ui/core/Paper";
import MenuList from "@material-ui/core/MenuList";
import MenuItem from "@material-ui/core/MenuItem";
import { withStyles } from '@material-ui/core/styles';


const StyledMenu = withStyles({
    root: {
        height: "600px",
        width: "250px",
        background: "rgba(255, 255, 255, .8)",
        boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
    },
})(MenuList);


const Menu = () => {

    return (
        <div>
        <Paper>
            <StyledMenu>

                <MenuItem onClick={(e) => {
                    e.preventDefault();
                    window.location.href = 'http://localhost:8000/';
                }}> Learning</MenuItem>

                <MenuItem onClick={(e) => {
                    e.preventDefault();
                    window.location.href = 'http://localhost:8000/register';
                }}> My account </MenuItem>

                <MenuItem onClick={(e) => {
                    e.preventDefault();
                    window.location.href = 'http://localhost:8000/register';
                }} > Ranking </MenuItem>

                <MenuItem onClick={(e) => {
                    e.preventDefault();
                    window.location.href = 'http://localhost:8000/logout';
                }} > Logout </MenuItem>

            </StyledMenu>
        </Paper>
        </div>

    )}

export default (Menu);

const container = document.getElementById("menu");
render(<Menu />, container);
