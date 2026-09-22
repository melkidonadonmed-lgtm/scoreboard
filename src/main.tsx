import React from 'react';
import ReactDOM from 'react-dom/client';
import { registerSW } from 'virtual:pwa-register';
import App from './App';
import './index.css';

registerSW({ immediate: true });

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Elemento raiz "root" não encontrado no DOM.');
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
