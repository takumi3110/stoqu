import logo from './logo.svg';
import './App.css';
import React from "react";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h2>yaa</h2>
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <div className="container">
          <table className="table table-hover">
            <thead>
            <tr>
              <th>a</th>
            </tr>
            </thead>
            <tbody>
            <tr>
              <td>
                td
              </td>
            </tr>
            </tbody>
          </table>
      </div>
      </header>
    </div>
);
}

export default App;
