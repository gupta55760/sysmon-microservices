'use strict';

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { 'default': obj }; }

var _react = require('react');

var _react2 = _interopRequireDefault(_react);
console.log(_react2)

function App() {
    return _react2['default'].createElement(
        'h1',
        null,
        ' Hello World'
    );
}

var myElement = _react2['default'].createElement(
    'h1',
    null,
    'Hello World'
);
var element = _react2['default'].createElement('h2', {}, 'Hello');
console.log(element);
