import {render} from "react-dom";
import React, {useEffect, useState} from "react";
import styled from 'styled-components'

const Menu = () => {
    const linksArray =
        [
        {name: "let's learn", url: "#"},
        {name: "ranking", url: "#"},
        {name: "asd", url: "#"},
        {name: "settings", url: "#"}
    ]

    console.log("asasdasd")

        return (
            <div>

                <Links links={linksArray} />
            </div>
        );
}

const Links = (props) => {
    console.log("asasdasd links")
        props.links.map((link) => (
            <li className="link">
                <a href={link.url}>{link.name}</a>
            </li>
            ));
    }


export default Menu;

const container = document.getElementById("menu");
render(<Menu />, container);

const LinkList = styled.ul`
  padding-top: 90px;
  padding-right: 25px;
  padding-left: 25px;
`

const Panel = styled.div`
  height: 600px;
  width: 250px;
  background-color: rgba(255, 255, 255, .8);
  margin-left: -450px;
  margin-top: -10px;
  opacity: 0;
  -webkit-box-shadow: 10px 10px 6px -8px rgba(161, 136, 119, .7);
  transition: all .3s ease-in-out;
  border-radius: 2px;
  padding: 0 auto;
  border-right: 1px solid rgba(0, 0, 0, .2);
  border-bottom: 1px solid rgba(0, 0, 0, .2);
  margin-left: 0px;
  opacity: 1;
`