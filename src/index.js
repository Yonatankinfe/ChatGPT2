import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import Header from './header';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  
  <React.StrictMode>
    <Header />
    <App />
    <div>
      <p className='par'>This webiste is an open source project for demonstrating chatgpt2.0 you can get the all the info and more at this link
        <a href='https://github.com/Yonatankinfe/ChatGPT2'> Click here</a></p>
    </div>
  </React.StrictMode>
);


reportWebVitals();
