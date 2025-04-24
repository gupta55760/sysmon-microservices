import React from 'react';
import ReactDOM from 'react-dom/client';

const myElement = <h1>I Love JSX!</h1>;
console.log("myElement is:", myElement)

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(myElement);

