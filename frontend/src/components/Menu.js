import React from 'react';
import {render} from "react-dom";

import Paper from "@material-ui/core/Paper";
import MenuList from "@material-ui/core/MenuList";
import MenuItem from "@material-ui/core/MenuItem";
import { withStyles } from '@material-ui/core/styles';


const StyledMenu = withStyles({
    root: {
        height: "100%",
        width: "200px",
        background: "rgba(255, 255, 255, .8)",
        boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
        padding: '200px 0 0 40px'
    },
})(MenuList);


const StyledMenuItem = withStyles({
    root: {
        margin: '20px 0 0 0'
    }
})(MenuItem);

const Menu = () => {

    return (
        <div>
        <Paper>
            <StyledMenu>

                <StyledMenuItem onClick={(e) => {
                    e.preventDefault();
                    window.location.href = 'http://localhost:8000/';
                }}> Learning</StyledMenuItem>

                <StyledMenuItem onClick={(e) => {
                    e.preventDefault();
                    window.location.href = 'http://localhost:8000/account';
                }}> My account </StyledMenuItem>

                <StyledMenuItem onClick={(e) => {
                    e.preventDefault();
                    window.location.href = 'http://localhost:8000/ranking';
                }} > Ranking </StyledMenuItem>

                <StyledMenuItem onClick={(e) => {
                    e.preventDefault();
                    window.location.href = 'http://localhost:8000/logout';
                }} > Logout </StyledMenuItem>

            </StyledMenu>
        </Paper>
        </div>

    )}

export default (Menu);

const container = document.getElementById("menu");
render(<Menu />, container);
