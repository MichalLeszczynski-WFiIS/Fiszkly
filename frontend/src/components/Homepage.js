import React, { useState, useEffect } from 'react';
import { render } from "react-dom";


function Homepage() {

    useEffect(() => {
        document.title = `Fiszkly`;
    });

    return (
        <div>
            <button>
                only test if it works, zmien sie, znowu
            </button>
        </div>
    );
}

export default Homepage;

const container = document.getElementById("homepage");
render(<Homepage />, container);
