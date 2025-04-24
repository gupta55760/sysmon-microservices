'use strict';

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _react = require('react');

var _react2 = _interopRequireDefault(_react);

var _reactDomClient = require('react-dom/client');

var _reactDomClient2 = _interopRequireDefault(_reactDomClient);

var myElement = _react2['default'].createElement(
  'h1',
  null,
  'I Love JSX!'
);
console.log("myElement is:", myElement);

var root = _reactDomClient2['default'].createRoot(document.getElementById('root'));
root.render(myElement);
