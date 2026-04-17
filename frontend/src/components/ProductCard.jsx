import React from 'react';

const ProductCard = ({ product, onClick }) => {
  return (
    <div 
      className="bg-card border border-border rounded-2xl cursor-pointer 
                 transition-all duration-300 ease-out
                 hover:-translate-y-2 hover:shadow-[0_12px_32px_rgba(173,70,255,0.15)] 
                 hover:border-primary/50 flex flex-col justify-between h-auto relative group overflow-hidden"
      onClick={() => onClick(product)}
    >
      <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10">
         <span className="bg-primary/90 text-primary-foreground border border-primary/20 text-xs px-2.5 py-1 rounded-full font-semibold uppercase tracking-wider flex items-center gap-1.5 shadow-sm">
           <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
           AI Optimized
         </span>
      </div>

      <div className="w-full h-48 bg-muted/20 relative">
        <img 
          src={product.image} 
          alt={product.name} 
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background/40 to-transparent"></div>
      </div>

      <div className="p-6 flex flex-col flex-grow">
        <div>
          <h3 className="font-bold text-foreground text-xl mb-1.5 leading-tight pr-8">{product.name}</h3>
          <p className="text-muted-foreground text-sm flex items-center gap-1.5">
            <span className="text-yellow-400 text-xs">★</span> {product.rating}
          </p>
        </div>
        
        <div className="mt-4 flex items-end justify-between self-start w-full">
          <span className="text-primary font-bold text-2xl tracking-tight">${product.price}</span>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
