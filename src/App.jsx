import React, { useState } from 'react';
import Home from './pages/Home';
import ProductPage from './pages/ProductPage';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [selectedProductId, setSelectedProductId] = useState(null);

  const navigate = (page, productId = null) => {
    setCurrentPage(page);
    if (productId !== null) {
      setSelectedProductId(productId);
    }
    // Scroll to top on navigation to simulate clean page load
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-background font-sans">
      {currentPage === 'home' && (
        <Home onNavigate={navigate} />
      )}
      {currentPage === 'product' && (
        <ProductPage 
          productId={selectedProductId} 
          onNavigate={navigate} 
        />
      )}
    </div>
  );
}

export default App;