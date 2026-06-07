import { useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';
import './style.css';
import Navbar from './components/Navbar';
import ServicesList from './pages/ServicesList';
import ServiceDetail from './pages/ServiceDetail';
import BankCart from './pages/BankCart';

function App() {
  const [cartItems, setCartItems] = useState<Set<number>>(new Set());
  const clearCart = () => setCartItems(new Set());

  return (
    <BrowserRouter future={{ v7_relativeSplatPath: true }}>
      <Navbar />
      <Routes>
        <Route
          path="/"
          element={<ServicesList cartItems={cartItems} setCartItems={setCartItems} />}
        />
        <Route path="/service/:id" element={<ServiceDetail />} />
        <Route
          path="/bank-cart"
          element={<BankCart cartItems={cartItems} clearCart={clearCart} />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;