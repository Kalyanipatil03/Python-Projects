'use client';

import React, { useContext, useState, useEffect } from 'react';
import { WishlistContext, useCart } from '../context/context';
import Link from 'next/link';

interface NavbarProps {
  activeTab?: string;
  setActiveTab?: (tab: string) => void;
  searchQuery?: string;
  setSearchQuery?: (q: string) => void;
}

export default function Navbar({ 
  activeTab = 'home', 
  setActiveTab,
  searchQuery = '',
  setSearchQuery
}: NavbarProps) {
  const { wishlist } = useContext(WishlistContext);
  const { cart } = useCart();

  // Modal & Auth States
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');

  // Form Fields
  const [name, setName] = useState('');
  const [identifier, setIdentifier] = useState(''); // Email or Mobile
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');

  // Logged in User State
  const [user, setUser] = useState<{ id: string; name: string } | null>(null);

  // Load saved user session on component mount
  useEffect(() => {
    const savedUser = localStorage.getItem('kickstore_user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleAuthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (authMode === 'register') {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email: identifier, phone, password }),
      });

      const data = await res.json();
      if (res.ok) {
        alert('Registration successful! You can now login.');
        setAuthMode('login');
      } else {
        alert(data.error || 'Registration failed');
      }
    } else {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identifier, password }),
      });

      const data = await res.json();
      if (res.ok) {
        setUser(data.user);
        localStorage.setItem('kickstore_user', JSON.stringify(data.user));
        setIsAuthModalOpen(false);
        resetForm();
      } else {
        alert(data.error || 'Invalid email/phone or password');
      }
    }
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('kickstore_user');
  };

  const resetForm = () => {
    setName('');
    setIdentifier('');
    setPassword('');
    setPhone('');
  };

  return (
    <>
      <nav style={styles.nav}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <h2 style={styles.logo} onClick={() => setActiveTab ? setActiveTab('home') : null}>
            <Link href="/" style={{ color: '#fff', textDecoration: 'none' }}>KickStore</Link>
          </h2>

          {setSearchQuery && (
            <input 
              type="text" 
              placeholder="Search shoes, brands..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={styles.searchBar}
            />
          )}
        </div>

        <div style={styles.menu}>
          <button 
            style={activeTab === 'home' ? styles.activeBtn : styles.btn} 
            onClick={() => setActiveTab ? setActiveTab('home') : null}
          >
            Home
          </button>

          <button 
            style={activeTab === 'wishlist' ? styles.activeBtn : styles.btn} 
            onClick={() => setActiveTab ? setActiveTab('wishlist') : null}
          >
            ❤️ Wishlist ({wishlist.length})
          </button>

          <Link href="/cart" style={{ textDecoration: 'none' }}>
            <button style={styles.btn}>
              🛒 Cart ({cart.reduce((a, c) => a + (c.quantity || 1), 0)})
            </button>
          </Link>

          {/* Displays Logged-in User Name or Login Button */}
          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <Link href="/orders" style={{ color: '#ffe500', textDecoration: 'none', fontSize: '14px', fontWeight: 'bold' }}>
                📦 My Orders
              </Link>
              <span style={{ fontWeight: 'bold', color: '#fff' }}>👤 {user.name}</span>
              <button onClick={handleLogout} style={styles.logoutBtn}>Logout</button>
            </div>
          ) : (
            <button 
              style={styles.loginBtn}
              onClick={() => setIsAuthModalOpen(true)}
            >
              Login / Register
            </button>
          )}
        </div>
      </nav>

      {/* AUTHENTICATION MODAL */}
      {isAuthModalOpen && (
        <div style={styles.modalOverlay} onClick={() => setIsAuthModalOpen(false)}>
          <div style={styles.modalContainer} onClick={(e) => e.stopPropagation()}>
            <button style={styles.closeBtn} onClick={() => setIsAuthModalOpen(false)}>✕</button>

            <div style={styles.modalContent}>
              <div style={styles.leftBanner}>
                <h2 style={{ fontSize: '24px', marginBottom: '16px' }}>
                  {authMode === 'login' ? 'Login' : 'Register'}
                </h2>
                <p style={{ fontSize: '14px', color: '#dbdbdb', lineHeight: '1.4' }}>
                  {authMode === 'login' 
                    ? 'Get access to your Orders, Wishlist and Recommendations' 
                    : 'Sign up to manage orders and explore shoes'}
                </p>
              </div>

              <div style={styles.rightForm}>
                <form onSubmit={handleAuthSubmit}>
                  {authMode === 'register' && (
                    <input
                      type="text"
                      required
                      placeholder="Full Name"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      style={styles.formInput}
                    />
                  )}

                  <input
                    type="text"
                    required
                    placeholder={authMode === 'register' ? 'Email Address' : 'Email or Mobile Number'}
                    value={identifier}
                    onChange={(e) => setIdentifier(e.target.value)}
                    style={styles.formInput}
                  />

                  {authMode === 'register' && (
                    <input
                      type="text"
                      required
                      placeholder="Mobile Number"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      style={styles.formInput}
                    />
                  )}

                  <input
                    type="password"
                    required
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={styles.formInput}
                  />

                  <button type="submit" style={styles.submitBtn}>
                    {authMode === 'login' ? 'Login' : 'Create Account'}
                  </button>
                </form>

                <div style={{ marginTop: '15px', textAlign: 'center' }}>
                  {authMode === 'login' ? (
                    <span style={{ fontSize: '13px', color: '#333' }}>
                      New to KickStore?{' '}
                      <button onClick={() => setAuthMode('register')} style={styles.switchBtn}>
                        Create an account
                      </button>
                    </span>
                  ) : (
                    <span style={{ fontSize: '13px', color: '#333' }}>
                      Already have an account?{' '}
                      <button onClick={() => setAuthMode('login')} style={styles.switchBtn}>
                        Login here
                      </button>
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  nav: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 30px', background: '#2874f0', color: '#fff' },
  logo: { margin: 0, cursor: 'pointer', fontSize: '22px', fontWeight: 'bold' },
  searchBar: { padding: '8px 15px', width: '280px', borderRadius: '4px', border: 'none', outline: 'none' },
  menu: { display: 'flex', gap: '15px', alignItems: 'center' },
  btn: { background: 'transparent', border: 'none', color: '#fff', fontSize: '15px', cursor: 'pointer', padding: '8px 12px' },
  activeBtn: { background: '#fff', color: '#2874f0', border: 'none', fontSize: '15px', cursor: 'pointer', padding: '8px 12px', borderRadius: '4px', fontWeight: 'bold' },
  loginBtn: { background: '#fff', color: '#2874f0', border: '1px solid #fff', padding: '6px 18px', fontWeight: 'bold', borderRadius: '2px', cursor: 'pointer' },
  logoutBtn: { background: 'transparent', color: '#fff', border: '1px solid #fff', padding: '4px 10px', fontSize: '12px', borderRadius: '2px', cursor: 'pointer' },
  modalOverlay: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.6)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 },
  modalContainer: { position: 'relative', width: '620px', minHeight: '420px', backgroundColor: '#fff', borderRadius: '4px', overflow: 'hidden', boxShadow: '0 4px 16px rgba(0,0,0,0.2)' },
  closeBtn: { position: 'absolute', top: '10px', right: '16px', background: 'none', border: 'none', fontSize: '20px', color: '#333', cursor: 'pointer', zIndex: 10 },
  modalContent: { display: 'flex', minHeight: '420px' },
  leftBanner: { width: '40%', backgroundColor: '#2874f0', color: '#fff', padding: '30px 24px', boxSizing: 'border-box' },
  rightForm: { width: '60%', padding: '30px', display: 'flex', flexDirection: 'column', justifyContent: 'center', boxSizing: 'border-box' },
  formInput: { width: '100%', padding: '10px 0', border: 'none', borderBottom: '1px solid #e0e0e0', fontSize: '14px', outline: 'none', marginBottom: '15px' },
  submitBtn: { width: '100%', background: '#fb641b', color: '#fff', border: 'none', padding: '12px', fontWeight: 'bold', fontSize: '14px', borderRadius: '2px', cursor: 'pointer', marginTop: '10px' },
  switchBtn: { background: 'none', border: 'none', color: '#2874f0', fontWeight: 'bold', cursor: 'pointer', padding: 0 }
};