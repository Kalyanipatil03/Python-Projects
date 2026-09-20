'use client';

import React, { useState, useEffect, useRef, useContext } from 'react';
import { WishlistContext, Shoe } from '../context/context';

interface ProductListProps {
  shoes: Shoe[];
}

const ProductList: React.FC<ProductListProps> = ({ shoes }) => {
  const { toggleWishlist, isLiked } = useContext(WishlistContext);
  
  const [categoryFilter, setCategoryFilter] = useState('All');
  const [visibleCount, setVisibleCount] = useState(8);
  const [feedback, setFeedback] = useState<string | null>(null);
  const loaderRef = useRef<HTMLDivElement | null>(null);

  const reviews = [
    { id: 1, name: "Aarav S.", shoe: "Nike Air Max", rating: "★★★★★", review: "Super comfortable for daily running!" },
    { id: 2, name: "Priya M.", shoe: "Puma Softfoam", rating: "★★★★☆", review: "Great value for money, highly recommended." },
    { id: 3, name: "Rohan K.", shoe: "Adidas Ultraboost", rating: "★★★★★", review: "Fits perfectly. Delivery was super fast." },
  ];

  const filteredShoes = shoes.filter((shoe) => {
    if (categoryFilter === 'All') return true;
    return shoe.category === categoryFilter;
  });

  useEffect(() => {
    setVisibleCount(8);
  }, [categoryFilter]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          setVisibleCount((prev) => prev + 4);
        }
      },
      { threshold: 1.0 }
    );

    if (loaderRef.current) observer.observe(loaderRef.current);
    return () => observer.disconnect();
  }, [filteredShoes]);

  const displayedShoes = filteredShoes.slice(0, visibleCount);

  return (
    <div style={{ padding: '20px' }}>
      {/* Category Filter */}
      <div style={styles.filterBar}>
        <label><strong>Filter Category: </strong></label>
        {['All', 'Running', 'Sneakers', 'Casual'].map((cat) => (
          <button 
            key={cat}
            onClick={() => setCategoryFilter(cat)}
            style={categoryFilter === cat ? styles.activeFilter : styles.filterBtn}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Shoes Grid */}
      <div style={styles.grid}>
        {displayedShoes.map((shoe) => {
          const liked = isLiked(shoe.id);
          return (
            <div key={shoe.id} style={styles.card}>
              <button 
                onClick={() => toggleWishlist(shoe)} 
                style={styles.heartBtn}
              >
                {liked ? '❤️' : '🤍'}
              </button>
              <img src={shoe.image} alt={shoe.name} style={styles.image} />
              <h3 style={styles.shoeName}>{shoe.name}</h3>
              <p style={styles.category}>{shoe.category}</p>
              <p style={styles.price}>₹{shoe.price}</p>
            </div>
          );
        })}
      </div>

      {/* Infinite Scroll Loader */}
      {visibleCount < filteredShoes.length && (
        <div ref={loaderRef} style={styles.loader}>
          Loading more shoes... 👟
        </div>
      )}

      {/* Feedback & Reviews */}
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

        <div style={{ marginTop: '30px' }}>
          <h2>Reviews for Popular Footwear</h2>
          <div style={styles.reviewsGrid}>
            {reviews.map((rev) => (
              <div key={rev.id} style={styles.reviewCard}>
                <div style={{ color: '#ff9900', fontWeight: 'bold' }}>{rev.rating}</div>
                <strong>{rev.shoe}</strong>
                <p style={{ fontStyle: 'italic', fontSize: '14px', margin: '8px 0' }}>"{rev.review}"</p>
                <small>- {rev.name}</small>
              </div>
            ))}
          </div>
        </div>
      </footer>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  filterBar: { marginBottom: '20px', display: 'flex', gap: '10px', alignItems: 'center' },
  filterBtn: { padding: '6px 12px', border: '1px solid #ccc', background: '#fff', cursor: 'pointer', borderRadius: '4px' },
  activeFilter: { padding: '6px 12px', border: '1px solid #2874f0', background: '#2874f0', color: '#fff', cursor: 'pointer', borderRadius: '4px' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '20px' },
  card: { border: '1px solid #eee', borderRadius: '8px', padding: '15px', position: 'relative', textAlign: 'center', background: '#fff' },
  heartBtn: { position: 'absolute', top: '10px', right: '10px', background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer' },
  image: { width: '100%', height: '160px', objectFit: 'cover', borderRadius: '4px' },
  shoeName: { fontSize: '16px', margin: '10px 0 5px 0' },
  category: { fontSize: '12px', color: '#777', margin: '0 0 8px 0' },
  price: { fontWeight: 'bold', color: '#2874f0', margin: 0 },
  loader: { textAlign: 'center', padding: '30px', fontWeight: 'bold', color: '#666' },
  footer: { marginTop: '50px', borderTop: '1px solid #ddd', paddingTop: '20px' },
  feedbackBox: { textAlign: 'center', background: '#f8f9fa', padding: '20px', borderRadius: '8px' },
  actionBtn: { margin: '0 10px', padding: '8px 20px', border: '1px solid #ccc', background: '#fff', cursor: 'pointer', borderRadius: '4px', fontWeight: 'bold' },
  reviewsGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '15px', marginTop: '15px' },
  reviewCard: { border: '1px solid #eee', padding: '15px', borderRadius: '8px', background: '#fafafa' }
};

export default ProductList;