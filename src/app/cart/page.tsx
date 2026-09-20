'use client';

import React from 'react';
import { useCart } from '../../context/context';
import Link from 'next/link';

export default function CartPage() {
  const { cart, clearCart, removeFromCart } = useCart();

  const subtotal = cart
    ? cart.reduce((sum: number, item: any) => sum + item.price * (item.quantity || 1), 0)
    : 0;
  const shipping = cart && cart.length > 0 ? 12.0 : 0;
  const total = subtotal + shipping;

  const handleCheckout = async () => {
    const savedUser = localStorage.getItem('kickstore_user');
    const user = savedUser ? JSON.parse(savedUser) : null;

    if (!user) {
      alert('Please log in first to place an order!');
      return;
    }

    if (!cart || cart.length === 0) {
      alert('Your cart is empty!');
      return;
    }

    try {
      const response = await fetch('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: user.id || user.email,
          items: cart,
          totalAmount: total,
        }),
      });

      const contentType = response.headers.get('content-type');

      if (response.ok && contentType?.includes('application/json')) {
        const data = await response.json();
        alert('Thank you for your order!');
        if (clearCart) clearCart();
      } else {
        if (contentType?.includes('application/json')) {
          const errorData = await response.json();
          alert(errorData.error || 'Failed to place order.');
        } else {
          console.error(
            `Request failed (${response.status} ${response.statusText}). Check if route /api/orders/route.js exists.`
          );
          alert('API route not found. Please restart your Next.js dev server.');
        }
      }
    } catch (error) {
      console.error('Checkout error:', error);
      alert('Something went wrong during checkout.');
    }
  };

  if (!cart || cart.length === 0) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <h2>Shopping Cart</h2>
        <p style={{ margin: '20px 0', color: '#666' }}>Your cart is empty right now.</p>
        <Link href="/">
          <button
            style={{
              padding: '10px 20px',
              background: '#2874f0',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            Shop KickStore
          </button>
        </Link>
      </div>
    );
  }

  return (
    <div
      style={{
        maxWidth: '900px',
        margin: '40px auto',
        padding: '20px',
        background: '#fff',
        borderRadius: '8px',
      }}
    >
      <h2>Shopping Cart</h2>

      <div style={{ marginTop: '20px' }}>
        {cart.map((item: any, idx: number) => (
          <div
            key={idx}
            style={{
              display: 'flex',
              justify: 'space-between',
              alignItems: 'center',
              borderBottom: '1px solid #eee',
              padding: '15px 0',
            }}
          >
            <div>
              <h3 style={{ margin: '0 0 5px 0' }}>{item.name}</h3>
              <p style={{ margin: 0, color: '#666', fontSize: '14px' }}>
                Quantity: {item.quantity || 1}
              </p>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
              <span style={{ fontWeight: 'bold' }}>
                ${(item.price * (item.quantity || 1)).toFixed(2)}
              </span>
              {removeFromCart && (
                <button
                  onClick={() => removeFromCart(item.id)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#d32f2f',
                    cursor: 'pointer',
                  }}
                >
                  Remove
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '30px', borderTop: '2px solid #eee', paddingTop: '20px' }}>
        <h3>Order Summary</h3>
        <div style={{ display: 'flex', justifyContent: 'space-between', margin: '8px 0' }}>
          <span>Subtotal</span>
          <span>${subtotal.toFixed(2)}</span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', margin: '8px 0' }}>
          <span>Shipping</span>
          <span>${shipping.toFixed(2)}</span>
        </div>
        <hr style={{ margin: '10px 0' }} />
        <div
          style={{
            display: 'flex',
            justify: 'space-between',
            margin: '8px 0',
            fontSize: '18px',
            fontWeight: 'bold',
          }}
        >
          <span>Total</span>
          <span>${total.toFixed(2)}</span>
        </div>

        <button
          onClick={handleCheckout}
          style={{
            width: '100%',
            marginTop: '20px',
            padding: '14px',
            background: '#fb641b',
            color: '#fff',
            border: 'none',
            fontSize: '16px',
            fontWeight: 'bold',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Checkout Now
        </button>
      </div>
    </div>
  );
}