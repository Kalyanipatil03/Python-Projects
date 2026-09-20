'use client';

import { useCart } from '@/context/context';
import { Heart, Star, Zap } from 'lucide-react';

interface ShoeProps {
  shoe: {
    id: string;
    name: string;
    brand: string;
    price: number;
    description: string;
    image: string;
    category: string;
    rating: number;
    isOffer: boolean;
    origin: string;
  };
}

export default function ShoeCard({ shoe }: ShoeProps) {
  const { addToCart, wishlist, toggleWishlist } = useCart();
  const isWishlisted = wishlist.includes(shoe.id);

  return (
    <div className="group bg-white rounded-md overflow-hidden border border-gray-200 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col relative">
      
      {/* Wishlist Heart Button */}
      <button
        onClick={() => toggleWishlist(shoe.id)}
        className="absolute top-2 right-2 z-10 p-1.5 rounded-full bg-white/90 shadow-md hover:scale-110 transition-transform"
      >
        <Heart
          className={`h-4 w-4 ${
            isWishlisted ? 'fill-red-500 text-red-500' : 'text-gray-400 hover:text-red-500'
          }`}
        />
      </button>

      {/* Image Area */}
      <div className="relative aspect-square bg-gray-50 overflow-hidden">
        <img
          src={shoe.image}
          alt={shoe.name}
          className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500"
        />
        <span className="absolute top-2 left-2 bg-indigo-900/80 text-white backdrop-blur-md px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">
          {shoe.brand}
        </span>
        {shoe.isOffer && (
          <span className="absolute bottom-2 left-2 bg-yellow-400 text-indigo-950 px-2 py-0.5 rounded text-[10px] font-extrabold flex items-center gap-0.5 shadow">
            <Zap className="h-3 w-3 fill-indigo-950" /> SPECIAL OFFER
          </span>
        )}
      </div>

      {/* Details Area */}
      <div className="p-4 flex flex-col flex-1">
        <div className="flex items-center justify-between mb-1">
          <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-wider">
            {shoe.category} • {shoe.origin}
          </span>
          <div className="flex items-center gap-1 bg-green-700 text-white text-[11px] font-bold px-1.5 py-0.5 rounded">
            <span>{shoe.rating}</span>
            <Star className="h-3 w-3 fill-white" />
          </div>
        </div>

        <h3 className="text-sm font-bold text-gray-900 group-hover:text-indigo-600 transition-colors line-clamp-1">
          {shoe.name}
        </h3>
        <p className="text-xs text-gray-500 line-clamp-2 mt-1 mb-3 flex-1">
          {shoe.description}
        </p>

        <div className="flex items-center justify-between pt-2 border-t border-gray-100 mt-auto">
          <div>
            <span className="text-base font-black text-gray-900">
              ${shoe.price.toFixed(2)}
            </span>
            <span className="text-[10px] text-gray-400 block line-through">
              ${(shoe.price * 1.3).toFixed(2)}
            </span>
          </div>
          <button
            onClick={() => addToCart(shoe)}
            className="bg-orange-500 hover:bg-orange-600 active:scale-95 text-white text-xs font-bold px-3.5 py-2 rounded shadow-sm transition-all"
          >
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
}