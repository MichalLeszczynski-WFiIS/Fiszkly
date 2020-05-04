import React from 'react';
import styled from 'styled-components'
import ReactDelayRender from 'react-delay-render';


const LoggingPanel = () => {

    return (
    <LoggingSection>
        <Button
            className="button-log"
            onClick={(e) => {
                e.preventDefault();
                window.location.href = 'http://localhost:8000/login';
            }}>
            Log In
        </Button>

        <Description> or </Description>

        <Button
            className="button-log"
            onClick={(e) => {
                e.preventDefault();
                window.location.href = 'http://localhost:8000/register';
            }}>
            Register
        </Button>

        <Description><p> to start! </p></Description>

    </LoggingSection>
    )}

export default ReactDelayRender({ delay: 1500 })(LoggingPanel);

const Button = styled.button`
     display:inline;
     padding:0.35em 1.2em;
     border:0.1em solid #bbc3cd;
     margin:auto;
     height: 40px;
     width: 90px;
     border-radius:0.4em;
     box-sizing: border-box;
     text-decoration:none;
     font-family:'Roboto',sans-serif;
     font-weight:300;
     color:#bbc3cd;
     font-size: 0.8em;
     text-align:center;
     transition: all 0.2s;
        &:hover {
             color:#bbc3cd;
             background-color:white;
        }
`;

const LoggingSection = styled.section`
    text-align: center
`

const Description = styled.div`
    -webkit-font-smoothing: antialiased;
    font-family: 'Lato', 'Lucida Grande', 'Lucida Sans Unicode', Tahoma, Sans-Serif, serif;
    color: white;
    text-align: center;
    font-size: 1.3em;
    text-shadow: 0px 0px 8px #bbc3cd;
`