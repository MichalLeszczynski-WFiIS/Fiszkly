import React, { Component } from "react";
import { render } from "react-dom";

class App extends Component {

    render() {
        return (
            <div> test test x3 </div>
    );
    }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
