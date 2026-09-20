'use client';

import React, { useState, useEffect, useRef, useContext } from 'react';
import { WishlistContext, useCart, Shoe } from '../context/context';
import Navbar from '../components/Navbar';

export interface ExtendedShoe extends Shoe {
  brand: string;
  gender: string;
  sizes: number[];
  color: string;
  discount: number;
  country: string;
  popularity: number;
  isNew?: boolean;
}

const ALL_SHOES: ExtendedShoe[] = [
  { id: 1, name: "Nike Air Max 270", brand: "Nike", category: "Running", price: 10995, rating: 4.5, image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80", gender: "Men", sizes: [7, 8, 9, 10], color: "Red", discount: 20, country: "Vietnam", popularity: 98, isNew: true },
  { id: 2, name: "Adidas Ultraboost 1.0", brand: "Adidas", category: "Running", price: 14999, rating: 4.8, image: "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=400&q=80", gender: "Men", sizes: [8, 9, 10, 11], color: "Black", discount: 15, country: "India", popularity: 95 },
  { id: 3, name: "Puma Softride Enzo", brand: "Puma", category: "Sneakers", price: 4500, rating: 4.2, image: "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&q=80", gender: "Unisex", sizes: [6, 7, 8, 9], color: "White", discount: 30, country: "India", popularity: 82 },
  { id: 4, name: "Reebok Classic Leather", brand: "Reebok", category: "Casual", price: 5999, rating: 4.0, image: "https://images.unsplash.com/photo-1539185441755-769473a23570?w=400&q=80", gender: "Men", sizes: [7, 8, 9], color: "White", discount: 10, country: "Vietnam", popularity: 78 },
  { id: 5, name: "Nike Revolution 6", brand: "Nike", category: "Running", price: 3695, rating: 4.3, image: "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=400&q=80", gender: "Women", sizes: [6, 7, 8], color: "Blue", discount: 40, country: "Indonesia", popularity: 88 },
  { id: 6, name: "Adidas Forum Low", brand: "Adidas", category: "Casual", price: 8999, rating: 4.6, image: "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&q=80", gender: "Unisex", sizes: [7, 8, 9, 10], color: "White", discount: 25, country: "Vietnam", popularity: 91, isNew: true },
  { id: 7, name: "Puma Smash v2", brand: "Puma", category: "Casual", price: 2999, rating: 4.1, image: "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400&q=80", gender: "Men", sizes: [6, 7, 8, 9, 10], color: "Red", discount: 50, country: "India", popularity: 75 },
  { id: 8, name: "Asics Gel-Kayano 28", brand: "Asics", category: "Running", price: 12999, rating: 4.7, image: "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=400&q=80", gender: "Men", sizes: [8, 9, 10], color: "Grey", discount: 20, country: "Vietnam", popularity: 93 },
  { id: 9, name: "New Balance 574", brand: "New Balance", category: "Sneakers", price: 7999, rating: 4.4, image: "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?w=400&q=80", gender: "Unisex", sizes: [7, 8, 9, 10, 11], color: "Grey", discount: 15, country: "Indonesia", popularity: 86 },
  { id: 10, name: "Skechers Go Walk 6", brand: "Skechers", category: "Casual", price: 4999, rating: 4.2, image: "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400&q=80", gender: "Women", sizes: [6, 7, 8], color: "Black", discount: 30, country: "China", popularity: 80 },
  { id: 11, name: "Converse Chuck Taylor", brand: "Converse", category: "Sneakers", price: 3999, rating: 4.5, image: "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400&q=80", gender: "Unisex", sizes: [6, 7, 8, 9, 10], color: "Black", discount: 10, country: "Vietnam", popularity: 97 },
  { id: 12, name: "Vans Old Skool Core", brand: "Vans", category: "Sneakers", price: 4500, rating: 4.6, image: "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&q=80", gender: "Unisex", sizes: [7, 8, 9, 10], color: "Black", discount: 20, country: "Vietnam", popularity: 94 },
  { id: 13, name: "Nike Pegasus 40", brand: "Nike", category: "Running", price: 11895, rating: 4.7, image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80", gender: "Men", sizes: [8, 9, 10, 11], color: "Blue", discount: 15, country: "Vietnam", popularity: 96, isNew: true },
  { id: 14, name: "Adidas NMD R1", brand: "Adidas", category: "Sneakers", price: 12999, rating: 4.5, image: "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=400&q=80", gender: "Men", sizes: [7, 8, 9, 10], color: "Black", discount: 35, country: "India", popularity: 89 },
  { id: 15, name: "Puma RS-X3", brand: "Puma", category: "Sneakers", price: 8999, rating: 4.3, image: "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&q=80", gender: "Unisex", sizes: [7, 8, 9], color: "White", discount: 40, country: "Vietnam", popularity: 84 },
  { id: 16, name: "Reebok Zig Kinetica", brand: "Reebok", category: "Running", price: 9999, rating: 4.4, image: "https://images.unsplash.com/photo-1539185441755-769473a23570?w=400&q=80", gender: "Men", sizes: [8, 9, 10], color: "Red", discount: 30, country: "Indonesia", popularity: 81 },
  { id: 17, name: "Asics GT-2000 10", brand: "Asics", category: "Running", price: 10999, rating: 4.6, image: "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=400&q=80", gender: "Women", sizes: [6, 7, 8, 9], color: "Blue", discount: 25, country: "Vietnam", popularity: 87 },
  { id: 18, name: "New Balance 327", brand: "New Balance", category: "Casual", price: 8499, rating: 4.5, image: "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?w=400&q=80", gender: "Women", sizes: [6, 7, 8], color: "Green", discount: 20, country: "Indonesia", popularity: 90, isNew: true },
  { id: 19, name: "Nike Downshifter 12", brand: "Nike", category: "Running", price: 4295, rating: 4.2, image: "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=400&q=80", gender: "Men", sizes: [7, 8, 9, 10, 11], color: "Grey", discount: 30, country: "India", popularity: 85 },
  { id: 20, name: "Adidas Stan Smith", brand: "Adidas", category: "Casual", price: 8599, rating: 4.7, image: "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&q=80", gender: "Unisex", sizes: [6, 7, 8, 9, 10], color: "White", discount: 15, country: "India", popularity: 99 },
  { id: 21, name: "Puma Future Rider", brand: "Puma", category: "Casual", price: 6999, rating: 4.3, image: "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400&q=80", gender: "Men", sizes: [7, 8, 9], color: "Green", discount: 40, country: "Vietnam", popularity: 79 },
  { id: 22, name: "Skechers Arch Fit", brand: "Skechers", category: "Running", price: 6499, rating: 4.4, image: "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400&q=80", gender: "Women", sizes: [6, 7, 8, 9], color: "Grey", discount: 20, country: "China", popularity: 83 },
  { id: 23, name: "Nike Court Vision Low", brand: "Nike", category: "Casual", price: 5695, rating: 4.4, image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80", gender: "Men", sizes: [7, 8, 9, 10], color: "White", discount: 25, country: "India", popularity: 92 },
  { id: 24, name: "Adidas Duramo SL", brand: "Adidas", category: "Running", price: 4999, rating: 4.1, image: "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=400&q=80", gender: "Men", sizes: [8, 9, 10], color: "Black", discount: 50, country: "India", popularity: 77 },
  { id: 25, name: "Puma Suede Classic", brand: "Puma", category: "Casual", price: 6499, rating: 4.6, image: "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&q=80", gender: "Unisex", sizes: [6, 7, 8, 9, 10], color: "Red", discount: 20, country: "Vietnam", popularity: 91 },
  { id: 26, name: "Converse Run Star Hike", brand: "Converse", category: "Sneakers", price: 8999, rating: 4.8, image: "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400&q=80", gender: "Women", sizes: [6, 7, 8], color: "White", discount: 15, country: "Vietnam", popularity: 96, isNew: true },
  { id: 27, name: "Vans Sk8-Hi", brand: "Vans", category: "Sneakers", price: 5999, rating: 4.5, image: "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&q=80", gender: "Unisex", sizes: [7, 8, 9, 10], color: "Black", discount: 20, country: "Vietnam", popularity: 88 },
  { id: 28, name: "Nike Air Force 1 '07", brand: "Nike", category: "Sneakers", price: 8195, rating: 4.9, image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80", gender: "Unisex", sizes: [7, 8, 9, 10, 11], color: "White", discount: 10, country: "Vietnam", popularity: 100 },
  { id: 29, name: "Asics Novablast 3", brand: "Asics", category: "Running", price: 13999, rating: 4.8, image: "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=400&q=80", gender: "Men", sizes: [8, 9, 10], color: "Green", discount: 15, country: "Vietnam", popularity: 92, isNew: true },
  { id: 30, name: "New Balance 2002R", brand: "New Balance", category: "Sneakers", price: 13999, rating: 4.7, image: "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?w=400&q=80", gender: "Men", sizes: [8, 9, 10, 11], color: "Grey", discount: 20, country: "Indonesia", popularity: 95 },
  { id: 31, name: "Kids Light-Up Sneaker", brand: "Puma", category: "Casual", price: 2499, rating: 4.3, image: "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&q=80", gender: "Kids", sizes: [6, 7], color: "Red", discount: 30, country: "India", popularity: 70 },
  { id: 32, name: "Reebok Club C 85", brand: "Reebok", category: "Casual", price: 6599, rating: 4.5, image: "https://images.unsplash.com/photo-1539185441755-769473a23570?w=400&q=80", gender: "Unisex", sizes: [7, 8, 9, 10], color: "White", discount: 25, country: "Vietnam", popularity: 87 },
  { id: 33, name: "Nike ZoomX Vaporfly", brand: "Nike", category: "Running", price: 19995, rating: 4.9, image: "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=400&q=80", gender: "Men", sizes: [8, 9, 10], color: "Green", discount: 10, country: "Vietnam", popularity: 98 },
  { id: 34, name: "Adidas Superstar", brand: "Adidas", category: "Casual", price: 8999, rating: 4.7, image: "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&q=80", gender: "Unisex", sizes: [6, 7, 8, 9, 10], color: "White", discount: 20, country: "India", popularity: 96 },
  { id: 35, name: "Skechers D'Lites", brand: "Skechers", category: "Casual", price: 5999, rating: 4.2, image: "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400&q=80", gender: "Women", sizes: [6, 7, 8], color: "White", discount: 35, country: "China", popularity: 76 },
  { id: 36, name: "Nike Metcon 8", brand: "Nike", category: "Running", price: 11895, rating: 4.6, image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80", gender: "Men", sizes: [8, 9, 10, 11], color: "Black", discount: 15, country: "Vietnam", popularity: 89 },
  { id: 37, name: "Puma Nitro Velocity", brand: "Puma", category: "Running", price: 10999, rating: 4.5, image: "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400&q=80", gender: "Men", sizes: [7, 8, 9, 10], color: "Blue", discount: 30, country: "India", popularity: 83 },
  { id: 38, name: "Adidas Gazelle", brand: "Adidas", category: "Casual", price: 8999, rating: 4.6, image: "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=400&q=80", gender: "Unisex", sizes: [6, 7, 8, 9], color: "Red", discount: 20, country: "Vietnam", popularity: 93 },
  { id: 39, name: "Asics Gel-Nimbus 25", brand: "Asics", category: "Running", price: 14999, rating: 4.9, image: "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=400&q=80", gender: "Men", sizes: [8, 9, 10], color: "Black", discount: 10, country: "Vietnam", popularity: 97, isNew: true },
  { id: 40, name: "New Balance 990v5", brand: "New Balance", category: "Running", price: 18999, rating: 4.8, image: "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?w=400&q=80", gender: "Men", sizes: [8, 9, 10, 11], color: "Grey", discount: 15, country: "Indonesia", popularity: 91 },
  { id: 41, name: "Vans Slip-On Classic", brand: "Vans", category: "Casual", price: 3999, rating: 4.4, image: "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&q=80", gender: "Unisex", sizes: [6, 7, 8, 9], color: "Black", discount: 25, country: "Vietnam", popularity: 86 },
  { id: 42, name: "Reebok Nano X2", brand: "Reebok", category: "Running", price: 8999, rating: 4.3, image: "https://images.unsplash.com/photo-1539185441755-769473a23570?w=400&q=80", gender: "Men", sizes: [8, 9, 10], color: "Blue", discount: 40, country: "India", popularity: 80 },
  { id: 43, name: "Nike Air Max 90", brand: "Nike", category: "Casual", price: 9295, rating: 4.7, image: "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=400&q=80", gender: "Men", sizes: [7, 8, 9, 10], color: "Grey", discount: 20, country: "Vietnam", popularity: 95 },
  { id: 44, name: "Puma Slipstream", brand: "Puma", category: "Sneakers", price: 7999, rating: 4.4, image: "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&q=80", gender: "Unisex", sizes: [7, 8, 9, 10], color: "White", discount: 30, country: "India", popularity: 82 },
  { id: 45, name: "Kids Running Star", brand: "Nike", category: "Running", price: 2995, rating: 4.2, image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80", gender: "Kids", sizes: [6, 7], color: "Blue", discount: 20, country: "India", popularity: 72 },
  { id: 46, name: "Adidas Samba OG", brand: "Adidas", category: "Casual", price: 10999, rating: 4.9, image: "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=400&q=80", gender: "Unisex", sizes: [7, 8, 9, 10], color: "White", discount: 10, country: "Vietnam", popularity: 99, isNew: true },
  { id: 47, name: "Skechers Max Cushioning", brand: "Skechers", category: "Running", price: 7499, rating: 4.5, image: "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400&q=80", gender: "Women", sizes: [6, 7, 8], color: "Black", discount: 25, country: "China", popularity: 81 },
  { id: 48, name: "Converse Weapon CX", brand: "Converse", category: "Sneakers", price: 7999, rating: 4.3, image: "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400&q=80", gender: "Men", sizes: [8, 9, 10], color: "Red", discount: 35, country: "Vietnam", popularity: 78 },
  { id: 49, name: "Asics Gel-Quantum 360", brand: "Asics", category: "Running", price: 15999, rating: 4.7, image: "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=400&q=80", gender: "Men", sizes: [8, 9, 10], color: "Grey", discount: 15, country: "Vietnam", popularity: 89 },
  { id: 50, name: "Puma Cali Dream", brand: "Puma", category: "Casual", price: 6999, rating: 4.5, image: "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&q=80", gender: "Women", sizes: [6, 7, 8], color: "White", discount: 30, country: "India", popularity: 86 }
];

export default function Home() {
  const [activeTab, setActiveTab] = useState('home');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Flipkart Sorting State
  const [sortBy, setSortBy] = useState<string>('relevance');

  // Filters Dashboard State
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedGenders, setSelectedGenders] = useState<string[]>([]);
  const [selectedBrands, setSelectedBrands] = useState<string[]>([]);
  const [selectedSizes, setSelectedSizes] = useState<number[]>([]);
  const [selectedColors, setSelectedColors] = useState<string[]>([]);
  const [minDiscount, setMinDiscount] = useState<number>(0);
  const [selectedCountries, setSelectedCountries] = useState<string[]>([]);
  const [minRating, setMinRating] = useState<number>(0);
  const [priceRange, setPriceRange] = useState<number>(20000);

  const [visibleCount, setVisibleCount] = useState(12);
  const [feedback, setFeedback] = useState<string | null>(null);

  const { wishlist, toggleWishlist, isLiked } = useContext(WishlistContext);
  const { addToCart } = useCart();
  const loaderRef = useRef<HTMLDivElement | null>(null);

  const reviews = [
    { id: 1, name: "Aarav S.", shoe: "Nike Air Max 270", rating: "★★★★★ (5.0)", review: "Super comfortable for daily running!" },
    { id: 2, name: "Priya M.", shoe: "Puma Softfoam", rating: "★★★★☆ (4.2)", review: "Great value for money, highly recommended." },
    { id: 3, name: "Rohan K.", shoe: "Adidas Ultraboost", rating: "★★★★★ (4.8)", review: "Fits perfectly. Delivery was super fast." },
  ];

  // Helper Array Toggle
  const toggleSelection = <T,>(item: T, list: T[], setList: (newVal: T[]) => void) => {
    setList(list.includes(item) ? list.filter((i) => i !== item) : [...list, item]);
  };

  const sourceShoes = activeTab === 'wishlist' 
    ? wishlist.map(item => ({
        ...item, 
        brand: item.name.split(' ')[0], 
        gender: "Unisex", 
        sizes: [7,8,9], 
        color: "Black", 
        discount: 10, 
        country: "India", 
        popularity: 90 
      })) 
    : ALL_SHOES;

  // Multi-Filter Engine
  const filteredShoes = sourceShoes.filter((shoe) => {
    const matchesCategory = selectedCategory === 'All' || shoe.category === selectedCategory;
    const matchesGender = selectedGenders.length === 0 || selectedGenders.includes(shoe.gender);
    const matchesBrand = selectedBrands.length === 0 || selectedBrands.includes(shoe.brand);
    const matchesSize = selectedSizes.length === 0 || selectedSizes.some(s => shoe.sizes.includes(s));
    const matchesColor = selectedColors.length === 0 || selectedColors.includes(shoe.color);
    const matchesDiscount = shoe.discount >= minDiscount;
    const matchesCountry = selectedCountries.length === 0 || selectedCountries.includes(shoe.country);
    const matchesPrice = shoe.price <= priceRange;
    const matchesRating = (shoe.rating || 0) >= minRating;
    const matchesSearch = shoe.name.toLowerCase().includes(searchQuery.toLowerCase());
    
    return matchesCategory && matchesGender && matchesBrand && matchesSize && 
           matchesColor && matchesDiscount && matchesCountry && matchesPrice && 
           matchesRating && matchesSearch;
  });

  // Flipkart Sorting Engine
  const sortedShoes = [...filteredShoes].sort((a, b) => {
    if (sortBy === 'lowToHigh') return a.price - b.price;
    if (sortBy === 'highToLow') return b.price - a.price;
    if (sortBy === 'popularity') return b.popularity - a.popularity;
    if (sortBy === 'newest') return (b.isNew ? 1 : 0) - (a.isNew ? 1 : 0);
    return 0; // relevance
  });

  useEffect(() => {
    setVisibleCount(12);
  }, [selectedCategory, selectedGenders, selectedBrands, selectedSizes, selectedColors, minDiscount, selectedCountries, priceRange, minRating, sortBy, searchQuery, activeTab]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          setVisibleCount((prev) => prev + 6);
        }
      },
      { threshold: 0.5 }
    );

    if (loaderRef.current) observer.observe(loaderRef.current);
    return () => observer.disconnect();
  }, [sortedShoes]);

  const displayedShoes = sortedShoes.slice(0, visibleCount);

  const resetFilters = () => {
    setSelectedCategory('All');
    setSelectedGenders([]);
    setSelectedBrands([]);
    setSelectedSizes([]);
    setSelectedColors([]);
    setMinDiscount(0);
    setSelectedCountries([]);
    setPriceRange(20000);
    setMinRating(0);
    setSortBy('relevance');
    setSearchQuery('');
  };

  return (
    <div style={{ background: '#f1f3f6', minHeight: '100vh' }}>
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
      />

      <div style={{ display: 'flex', padding: '12px', gap: '12px', maxWidth: '1440px', margin: '0 auto' }}>
        
        {/* INDEPENDENT STICKY SCROLLING FILTERS DASHBOARD */}
        <aside style={styles.sidebar}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #eee', paddingBottom: '10px' }}>
            <h3 style={{ margin: 0, fontSize: '16px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Filters</h3>
            <button onClick={resetFilters} style={styles.resetTextBtn}>CLEAR ALL</button>
          </div>

          {/* Gender Filter */}
          <div style={styles.filterGroup}>
            <label style={styles.groupTitle}>Gender</label>
            {['Men', 'Women', 'Unisex', 'Kids'].map((g) => (
              <label key={g} style={styles.checkboxLabel}>
                <input 
                  type="checkbox" 
                  checked={selectedGenders.includes(g)}
                  onChange={() => toggleSelection(g, selectedGenders, setSelectedGenders)}
                />
                {g}
              </label>
            ))}
          </div>

          {/* Category Filter */}
          <div style={styles.filterGroup}>
            <label style={styles.groupTitle}>Category</label>
            {['All', 'Running', 'Sneakers', 'Casual'].map((cat) => (
              <label key={cat} style={styles.checkboxLabel}>
                <input 
                  type="radio" 
                  name="category"
                  checked={selectedCategory === cat}
                  onChange={() => setSelectedCategory(cat)}
                />
                {cat}
              </label>
            ))}
          </div>

          {/* Brand Filter */}
          <div style={styles.filterGroup}>
            <label style={styles.groupTitle}>Brand</label>
            {['Nike', 'Adidas', 'Puma', 'Reebok', 'Asics', 'New Balance', 'Skechers', 'Converse', 'Vans'].map((brand) => (
              <label key={brand} style={styles.checkboxLabel}>
                <input 
                  type="checkbox" 
                  checked={selectedBrands.includes(brand)}
                  onChange={() => toggleSelection(brand, selectedBrands, setSelectedBrands)}
                />
                {brand}
              </label>
            ))}
          </div>

          {/* Size (UK) Filter */}
          <div style={styles.filterGroup}>
            <label style={styles.groupTitle}>Size (UK)</label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              {[6, 7, 8, 9, 10, 11].map((sz) => {
                const active = selectedSizes.includes(sz);
                return (
                  <button
                    key={sz}
                    onClick={() => toggleSelection(sz, selectedSizes, setSelectedSizes)}
                    style={{
                      padding: '6px 12px',
                      border: active ? '1px solid #2874f0' : '1px solid #ccc',
                      background: active ? '#2874f0' : '#fff',
                      color: active ? '#fff' : '#333',
                      borderRadius: '2px',
                      cursor: 'pointer',
                      fontSize: '12px',
                      fontWeight: 'bold'
                    }}
                  >
                    UK {sz}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Color Filter */}
          <div style={styles.filterGroup}>
            <label style={styles.groupTitle}>Color</label>
            {['Black', 'White', 'Blue', 'Red', 'Grey', 'Green'].map((color) => (
              <label key={color} style={styles.checkboxLabel}>
                <input 
                  type="checkbox" 
                  checked={selectedColors.includes(color)}
                  onChange={() => toggleSelection(color, selectedColors, setSelectedColors)}
                />
                {color}
              </label>
            ))}
          </div>

          {/* Discount Offer */}
          <div style={styles.filterGroup}>
            <label style={styles.groupTitle}>Discount Offer</label>
            {[10, 20, 30, 50].map((disc) => (
              <label key={disc} style={styles.checkboxLabel}>
                <input 
                  type="radio" 
                  name="discount"
                  checked={minDiscount === disc}
                  onChange={() => setMinDiscount(disc)}
                />
                {disc}% or more
              </label>
            ))}
            {minDiscount > 0 && (
              <button onClick={() => setMinDiscount(0)} style={styles.clearSubBtn}>Clear Discount</button>
            )}
          </div>

          {/* Country of Origin */}
          <div style={styles.filterGroup}>
            <label style={styles.groupTitle}>Country of Origin</label>
            {['India', 'Vietnam', 'Indonesia', 'China'].map((cntry) => (
              <label key={cntry} style={styles.checkboxLabel}>
                <input 
                  type="checkbox" 
                  checked={selectedCountries.includes(cntry)}
                  onChange={() => toggleSelection(cntry, selectedCountries, setSelectedCountries)}
                />
                {cntry}
              </label>
            ))}
          </div>

          {/* Max Price Range */}
          <div style={styles.filterGroup}>
            <label style={styles.groupTitle}>Max Price: ₹{priceRange.toLocaleString('en-IN')}</label>
            <input 
              type="range" 
              min="2000" 
              max="20000" 
              step="500"
              value={priceRange} 
              onChange={(e) => setPriceRange(Number(e.target.value))}
              style={{ width: '100%' }}
            />
          </div>

          {/* Minimum Rating */}
          <div style={styles.filterGroup}>
            <label style={styles.groupTitle}>Customer Rating</label>
            {[4.5, 4.0, 3.5].map((stars) => (
              <label key={stars} style={styles.checkboxLabel}>
                <input 
                  type="radio" 
                  name="rating"
                  checked={minRating === stars}
                  onChange={() => setMinRating(stars)}
                />
                {stars}★ & above
              </label>
            ))}
            {minRating > 0 && (
              <button onClick={() => setMinRating(0)} style={styles.clearSubBtn}>Clear Rating</button>
            )}
          </div>
        </aside>

        {/* MAIN PRODUCT DASHBOARD */}
        <main style={{ flex: 1, minWidth: 0 }}>
          
          {/* FLIPKART TOP SORTING BAR */}
          <div style={styles.flipkartSortBar}>
            <span style={styles.sortTitle}>Sort By</span>
            {[
              { id: 'relevance', label: 'Relevance' },
              { id: 'popularity', label: 'Popularity' },
              { id: 'lowToHigh', label: 'Price -- Low to High' },
              { id: 'highToLow', label: 'Price -- High to Low' },
              { id: 'newest', label: 'Newest First' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setSortBy(tab.id)}
                style={{
                  ...styles.sortTab,
                  color: sortBy === tab.id ? '#2874f0' : '#212121',
                  fontWeight: sortBy === tab.id ? 'bold' : 'normal',
                  borderBottom: sortBy === tab.id ? '2px solid #2874f0' : '2px solid transparent',
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <p style={{ margin: '10px 0 15px 0', fontSize: '14px', color: '#878787' }}>
            Showing {displayedShoes.length} of {sortedShoes.length} products
          </p>

          {displayedShoes.length === 0 ? (
            <div style={{ background: '#fff', padding: '50px', textAlign: 'center', borderRadius: '4px' }}>
              <h3>No shoes match your selected filters</h3>
              <button onClick={resetFilters} style={styles.actionBtn}>Clear All Filters</button>
            </div>
          ) : (
            <div style={styles.grid}>
              {displayedShoes.map((shoe) => {
                const liked = isLiked(shoe.id);
                const originalPrice = Math.round(shoe.price / (1 - shoe.discount / 100));

                return (
                  <div key={shoe.id} style={styles.card}>
                    <button 
                      onClick={() => toggleWishlist(shoe)} 
                      style={styles.heartBtn}
                      title="Add to Wishlist"
                    >
                      {liked ? '❤️' : '🤍'}
                    </button>
                    
                    <img src={shoe.image} alt={shoe.name} style={styles.image} />
                    
                    <small style={{ color: '#878787', fontWeight: 'bold' }}>{shoe.brand}</small>
                    <h4 style={styles.shoeName}>{shoe.name}</h4>
                    
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', margin: '4px 0' }}>
                      <div style={styles.ratingBadge}>
                        {shoe.rating || 4.2} ★
                      </div>
                      <span style={{ fontSize: '12px', color: '#878787' }}>({shoe.popularity * 12})</span>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', margin: '8px 0' }}>
                      <span style={styles.price}>₹{shoe.price.toLocaleString('en-IN')}</span>
                      <span style={styles.originalPrice}>₹{originalPrice.toLocaleString('en-IN')}</span>
                      <span style={styles.discountText}>{shoe.discount}% off</span>
                    </div>

                    <p style={{ fontSize: '11px', color: '#388e3c', margin: '0 0 10px 0', fontWeight: 'bold' }}>
                      Free delivery • {shoe.country}
                    </p>

                    <button 
                      onClick={() => addToCart(shoe)}
                      style={styles.cartBtn}
                    >
                      ADD TO CART
                    </button>
                  </div>
                );
              })}
            </div>
          )}

          {/* Infinite Scroll Indicator */}
          {visibleCount < sortedShoes.length && (
            <div ref={loaderRef} style={styles.loader}>
              Loading more shoes... 👟
            </div>
          )}

          {/* FLIPKART FOOTER REVIEWS & FEEDBACK */}
          <footer style={styles.footer}>
            <div style={styles.feedbackBox}>
              <h3>Did you find what you were looking for?</h3>
              {feedback ? (
                <p style={{ color: '#28a745', fontWeight: 'bold' }}>Thank you for your feedback! 👍</p>
              ) : (
                <div>
                  <button onClick={() => setFeedback('yes')} style={styles.actionBtn}>Yes</button>
                  <button onClick={() => setFeedback('no')} style={styles.actionBtn}>No</button>
                </div>
              )}
            </div>

            <div style={{ marginTop: '25px' }}>
              <h3>Reviews for Popular Footwear</h3>
              <div style={styles.reviewsGrid}>
                {reviews.map((rev) => (
                  <div key={rev.id} style={styles.reviewCard}>
                    <div style={{ color: '#388e3c', fontWeight: 'bold' }}>{rev.rating}</div>
                    <strong>{rev.shoe}</strong>
                    <p style={{ fontStyle: 'italic', fontSize: '13px', margin: '6px 0', color: '#555' }}>"{rev.review}"</p>
                    <small style={{ color: '#888' }}>- {rev.name}</small>
                  </div>
                ))}
              </div>
            </div>
          </footer>
        </main>
      </div>
    </div>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  // INDEPENDENT SIDEBAR SCROLL
  sidebar: { 
    width: '270px', 
    background: '#fff', 
    padding: '15px', 
    borderRadius: '4px', 
    position: 'sticky', 
    top: '10px', 
    maxHeight: '92vh', 
    overflowY: 'auto',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    flexShrink: 0
  },
  resetTextBtn: { background: 'none', border: 'none', color: '#2874f0', cursor: 'pointer', fontWeight: 'bold', fontSize: '12px' },
  filterGroup: { marginTop: '16px', borderTop: '1px solid #f0f0f0', paddingTop: '12px' },
  groupTitle: { fontWeight: 'bold', display: 'block', marginBottom: '8px', fontSize: '13px', textTransform: 'uppercase', color: '#212121' },
  checkboxLabel: { display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '13px', color: '#333', marginBottom: '6px' },
  clearSubBtn: { border: 'none', background: 'none', color: '#2874f0', fontSize: '12px', cursor: 'pointer', marginTop: '4px' },
  
  // FLIPKART TOP SORT BAR
  flipkartSortBar: { display: 'flex', alignItems: 'center', background: '#fff', padding: '12px 16px', borderRadius: '4px', gap: '20px', borderBottom: '1px solid #f0f0f0' },
  sortTitle: { fontWeight: 'bold', fontSize: '14px', color: '#212121' },
  sortTab: { 
    background: 'none', 
    borderTop: 'none',
    borderLeft: 'none',
    borderRight: 'none',
    fontSize: '14px', 
    cursor: 'pointer', 
    paddingBottom: '4px' 
  },

  // PRODUCT GRID
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(230px, 1fr))', gap: '12px' },
  card: { border: '1px solid #f0f0f0', borderRadius: '4px', padding: '12px', position: 'relative', background: '#fff', transition: 'box-shadow 0.2s' },
  heartBtn: { position: 'absolute', top: '10px', right: '10px', background: 'none', border: 'none', fontSize: '18px', cursor: 'pointer', zIndex: 2 },
  image: { width: '100%', height: '170px', objectFit: 'cover', borderRadius: '4px' },
  shoeName: { fontSize: '14px', margin: '2px 0 6px 0', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', fontWeight: 'normal' },
  ratingBadge: { display: 'inline-block', background: '#388e3c', color: '#fff', fontSize: '11px', fontWeight: 'bold', padding: '2px 6px', borderRadius: '3px' },
  price: { fontWeight: 'bold', fontSize: '16px', color: '#212121' },
  originalPrice: { fontSize: '13px', color: '#878787', textDecoration: 'line-through' },
  discountText: { fontSize: '13px', color: '#388e3c', fontWeight: 'bold' },
  cartBtn: { width: '100%', padding: '9px', background: '#ff9f00', color: '#fff', border: 'none', borderRadius: '2px', fontWeight: 'bold', cursor: 'pointer', fontSize: '12px' },
  loader: { textAlign: 'center', padding: '20px', fontWeight: 'bold', color: '#666' },
  footer: { marginTop: '30px', background: '#fff', padding: '20px', borderRadius: '4px' },
  feedbackBox: { textAlign: 'center', background: '#f8f9fa', padding: '15px', borderRadius: '4px' },
  actionBtn: { margin: '10px 10px 0 10px', padding: '8px 24px', border: '1px solid #ccc', background: '#fff', cursor: 'pointer', borderRadius: '2px', fontWeight: 'bold' },
  reviewsGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '12px' },
  reviewCard: { border: '1px solid #eee', padding: '12px', borderRadius: '4px', background: '#fbfbfb' }
};