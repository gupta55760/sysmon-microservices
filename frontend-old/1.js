import React from 'react';

function App() {
    return <h1> Hello World</h1>
}

const myElement = <h1>Hello World</h1>;
const element = React.createElement('h2', {}, 'Hello');
console.log(element)

