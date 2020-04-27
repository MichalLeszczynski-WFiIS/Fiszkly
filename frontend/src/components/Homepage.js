import React, { useState, useEffect } from 'react';
import { render } from "react-dom";
import LoggingPanel from "./LoggingPanel";


const Homepage = () => {

    useEffect(() => {
        document.title = `Fiszkly`;
    });

    return (
        <div>
            <LoggingPanel/>
        </div>
    );
}

export default Homepage;

const container = document.getElementById("homepage");
render(<Homepage />, container);
