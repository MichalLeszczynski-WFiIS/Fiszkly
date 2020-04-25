import React, { useState, useEffect } from 'react';
import { render } from "react-dom";


function App() {

    useEffect(() => {
        document.title = `test`;
    });

    return (
        <div>
            <button>
                Kliknij mnie
            </button>
        </div>
    );
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
