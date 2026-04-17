import React from 'react';
import ProductCard from '../components/ProductCard';
import { products } from '../data/mockData';

const Home = ({ onNavigate }) => {
  return (
    <div className="max-w-7xl mx-auto px-6 py-16">
      <div className="mb-16 text-center max-w-3xl mx-auto">
        <h1 className="text-5xl md:text-6xl font-extrabold text-foreground mb-6 tracking-tighter">
          Buy smarter. <span className="text-primary">Not more.</span>
        </h1>
        <p className="text-muted-foreground text-lg md:text-xl font-medium leading-relaxed">
          Our AI filters out overhyped products and highlights what actually adds long-term value.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {products.map((product) => (
          <ProductCard 
            key={product.id} 
            product={product} 
            onClick={(selected) => onNavigate('product', selected.id)} 
          />
        ))}
      </div>
    </div>
  );
};

export default Home;
