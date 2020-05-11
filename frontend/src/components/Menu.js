import {render} from "react-dom";
import React from "react";
import styled from 'styled-components'

const Menu = () => ({

    // getInitialState: function () {
    //     return { open: true };
    // },
    //
    // toggleMenu: function () {
    //     this.setState({ open: !this.state.open });
    // },

    render: function () {
        const linksArray = [
            { name: "let's learn", url: "#" },
            { name: "ranking", url: "#" },
            { name: "asd", url: "#" },
            { name: "settings", url: "#" }
        ];

        return (
            <div>
                <Panel
                    // open={this.state.open}
                    links={linksArray}
                />
                {/*<Button*/}
                {/*    // toggle={this.toggleMenu}*/}
                {/*    // open={this.state.open}*/}
                {/*/>*/}
            </div>
        );
    }
});

// const Button = () => ({
//     render: function () {
//         return (
//             <button
//                 className={this.props.open
//                     ? "menu-toggle close-button"
//                     : "menu-toggle "}
//                 onClick={this.props.toggle}
//             > <i className="fa fa-plus"></i>
//             </button>
//         );
//     }
// });

const Panel = () => ({
    render: function () {
        return (
            <div
                className={this.props.open
                    ? "menu-wrapper menu-open"
                    : "menu-wrapper"}
            >
                <Links
                    links={this.props.links}
                    // open={this.props.open}
                />
            </div>
        );
    }
});

const Links = () => ({
    render: function () {
        const linkList = this.props.links.map((link) => (
            <li className="link">
                <a href={link.url}>{link.name}</a>
            </li>
        ));

        return (
            <div
                className={this.props.open
                    ? "links-wrapper"
                    : "links-wrapper links-wrapper-closed"}
            >
                <ul className="link-list">
                {linkList}
            </ul>
                {/*<LinkList >*/}
                {/*    <ul>*/}
                {/*    {linkList}*/}
                {/*</ul>*/}
                {/*</LinkList>*/}
            </div>
        );
    }
});

export default Menu;


const container = document.getElementById("menu");
render(<Menu />, container);

const LinkList = styled.ul`
  padding-top: 90px;
  padding-right: 25px;
  padding-left: 25px;
`