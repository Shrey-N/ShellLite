// ShellLite Runtime (JS)
const fs = require('fs');
const path = require('path');
const https = require('https');
const { execSync } = require('child_process');

// Builtins
const say = console.log;
const print = console.log;
const range = (n) => [...Array(n).keys()];
const int = (x) => parseInt(x);
const str = (x) => String(x);
const float = (x) => parseFloat(x);
const len = (x) => x.length;

// Utils
const _slang_download = (url) => { console.log('Download not impl in minimal JS runtime'); };

// --- User Code ---

console.log('Testing JS Compiler');
var x = 10;
var y = 20;
console.log(('Sum: ' + (x + y)));
var items = ['Apple', 'Banana'];
for (let _i_475 = 0; _i_475 < 2; _i_475++) {
    console.log('Looping...');
}
for (let fruit of items) {
    console.log(('Item: ' + fruit));
}
var vscode = require('vscode');
console.log('Required vscode module');