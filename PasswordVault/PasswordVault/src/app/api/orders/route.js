import { NextResponse } from 'next/server';

// Temporary in-memory order storage
export let ordersDatabase = [];

export async function POST(req) {
  try {
    const { userId, items, totalAmount } = await req.json();

    if (!items || items.length === 0) {
      return NextResponse.json({ error: 'Cart is empty' }, { status: 400 });
    }

    const newOrder = {
      id: `ORD-${Date.now()}`,
      userId: userId || 'guest',
      items,
      totalAmount,
      createdAt: new Date().toISOString(),
    };

    ordersDatabase.push(newOrder);

    return NextResponse.json(
      { message: 'Order placed successfully', order: newOrder },
      { status: 201 }
    );
  } catch (error) {
    return NextResponse.json({ error: 'Failed to save order' }, { status: 500 });
  }
}

export async function GET(req) {
  const { searchParams } = new URL(req.url);
  const userId = searchParams.get('userId');

  const userOrders = ordersDatabase.filter((order) => order.userId === userId);
  return NextResponse.json({ orders: userOrders }, { status: 200 });
}