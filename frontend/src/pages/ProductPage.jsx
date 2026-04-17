import React, { useCallback, useEffect, useState } from 'react';
import BundleBox from '../components/BundleBox';
import { products } from '../data/mockData';

const ProductPage = ({ productId, onNavigate }) => {
  const [product, setProduct] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const analyzeProduct = useCallback(async (productToAnalyze, signal) => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(productToAnalyze),
        signal
      });

      if (!response.ok) {
        throw new Error(`Analyze request failed with status ${response.status}`);
      }

      const data = await response.json();
      setAnalysisData(data || null);
    } catch (requestError) {
      if (requestError.name === 'AbortError') {
        return;
      }

      setAnalysisData(null);
      setError('Failed to analyze product. Please try again.');
    } finally {
      if (!signal || !signal.aborted) {
        setLoading(false);
      }
    }
  }, []);

  useEffect(() => {
    const foundProduct = products.find((p) => p.id === productId) || null;
    setProduct(foundProduct);
    setAnalysisData(null);
    setError('');

    if (!foundProduct) {
      setLoading(false);
      return;
    }

    const controller = new AbortController();
    analyzeProduct(foundProduct, controller.signal);

    return () => controller.abort();
  }, [productId, analyzeProduct]);

  if (!product) {
    return (
      <div className="max-w-5xl mx-auto px-6 py-12 animate-in fade-in duration-500 ease-out">
        <button
          onClick={() => onNavigate('home')}
          className="group flex items-center text-muted hover:text-primary mb-10 text-sm font-bold uppercase tracking-widest transition-colors"
        >
          <span className="mr-2 transform group-hover:-translate-x-1 transition-transform">←</span> Return
        </button>
        <div className="bg-card border border-border rounded-2xl p-8 text-center text-muted-foreground font-medium">
          Product not found.
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-12 animate-in fade-in duration-500 ease-out">
      <button 
        onClick={() => onNavigate('home')}
        className="group flex items-center text-muted hover:text-primary mb-10 text-sm font-bold uppercase tracking-widest transition-colors"
      >
        <span className="mr-2 transform group-hover:-translate-x-1 transition-transform">←</span> Return
      </button>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 bg-card border border-border rounded-[2rem] p-10 mb-12 shadow-sm">
        <div className="aspect-square bg-muted/20 rounded-2xl flex items-center justify-center border border-border/50 relative overflow-hidden">
          <div className="absolute top-4 left-4 bg-primary/90 text-primary-foreground border border-primary/20 text-xs px-2.5 py-1 rounded-full font-semibold uppercase tracking-wider flex items-center gap-1.5 shadow-sm z-10">
            <span className="w-1.5 h-1.5 rounded-full bg-white shadow-[0_0_8px_rgba(255,255,255,0.8)]"></span>
            AI Checked
          </div>
          <img 
            src={product.image} 
            alt={product.name} 
            className="w-full h-full object-cover" 
          />
          <div className="absolute inset-0 bg-gradient-to-t from-background/20 to-transparent"></div>
        </div>
        
        <div className="flex flex-col justify-center">
          <div className="text-xs font-bold text-primary uppercase tracking-[0.2em] mb-3">Target Analysis</div>
          <h1 className="text-4xl md:text-5xl font-extrabold text-foreground tracking-tight mb-5 leading-tight">{product.name}</h1>
          <div className="flex items-center gap-2 mb-8 text-yellow-400">
            {'★'.repeat(Math.round(product.rating))} 
            <span className="text-muted-foreground ml-1.5 text-sm font-medium">({product.rating} verified score)</span>
          </div>
          <p className="text-4xl font-semibold text-primary mb-10">${product.price}</p>
          <button
            disabled
            className="bg-primary hover:bg-primary/90 text-primary-foreground py-4 px-8 rounded-xl font-bold uppercase tracking-widest w-full lg:w-max active:scale-[0.98] transition-all shadow-[0_8px_24px_rgba(173,70,255,0.25)] disabled:opacity-70 disabled:cursor-not-allowed"
          >
            Analyze Product
          </button>
        </div>
      </div>

      <div className="max-w-2xl">
        {loading ? (
          <div className="bg-card border border-border rounded-2xl p-10 flex flex-col items-center justify-center text-muted-foreground min-h-[240px]">
            <div className="w-8 h-8 border-2 border-border border-t-primary rounded-full animate-spin mb-5"></div>
            <p className="animate-pulse font-medium tracking-wide uppercase text-sm">Analyzing real-world usage patterns...</p>
          </div>
        ) : error ? (
          <div className="bg-card border border-border rounded-2xl p-10 flex flex-col items-center justify-center text-destructive min-h-[240px]">
            <p className="font-medium tracking-wide uppercase text-sm">Failed to analyze product. Please try again.</p>
          </div>
        ) : analysisData ? (
          <BundleBox data={analysisData} />
        ) : (
          <div className="bg-card border border-border rounded-2xl p-10 text-center text-muted-foreground font-medium min-h-[240px] flex items-center justify-center">
            No analysis available.
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductPage;
