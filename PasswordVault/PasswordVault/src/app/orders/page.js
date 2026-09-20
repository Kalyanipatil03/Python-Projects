'use client';

import React, { useEffect, useState } from 'react';

export default function OrderHistory() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedUser = localStorage.getItem('kickstore_user');
    if (savedUser) {
      const user = JSON.parse(savedUser);
      const userId = user.id || user.email;
      
      fetch(`/api/orders?userId=${encodeURIComponent(userId)}`)
        .then(async (res) => {
          const contentType = res.headers.get('content-type');
          if (contentType && contentType.includes('application/json')) {
            return res.json();
          }
          throw new Error('Non-JSON response received');
        })
        .then((data) => {
          setOrders(data.orders || []);
          setLoading(false);
        })
        .catch((err) => {
          console.error('Failed to load orders:', err);
          setOrders([]);
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  if (loading) {
    return <div style={{ textAlign: 'center', padding: '40px' }}>Loading your orders...</div>;
  }

  return (
    <div style={{ maxWidth: '800px', margin: '40px auto', padding: '20px', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
      <h2 style={{ marginBottom: '20px', color: '#2874f0' }}>📦 My Order History</h2>
      {orders.length === 0 ? (
        <p style={{ color: '#666' }}>No past orders found.</p>
      ) : (
        orders.map((order) => (
          <div key={order.id} style={{ border: '1px solid #e0e0e0', padding: '16px', marginBottom: '16px', borderRadius: '6px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #f0f0f0', paddingBottom: '8px', marginBottom: '12px' }}>
              <span style={{ fontWeight: 'bold' }}>Order ID: #{order.id}</span>
              <span style={{ color: '#888', fontSize: '13px' }}>
                {order.createdAt ? new Date(order.createdAt).toLocaleDateString() : 'Recent'}
              </span>
            </div>

            <div style={{ marginBottom: '12px' }}>
              <strong>Items Ordered:</strong>
              {order.items && order.items.map((item, i) => (
                <div key={i} style={{ fontSize: '14px', margin: '6px 0 6px 12px', color: '#333' }}>
                  • <strong>{item.name}</strong> (Qty: {item.quantity || 1}) - ${(item.price * (item.quantity || 1)).toFixed(2)}
                </div>
              ))}
            </div>

            <div style={{ textAlign: 'right', borderTop: '1px solid #eee', paddingTop: '8px', marginTop: '8px', fontSize: '15px' }}>
              <strong>Total Paid: </strong>
              <span style={{ color: '#2e7d32', fontWeight: 'bold', fontSize: '16px' }}>
                ${Number(order.totalAmount).toFixed(2)}
              </span>
            </div>
          </div>
        ))
      )}
    </div>
  );
}