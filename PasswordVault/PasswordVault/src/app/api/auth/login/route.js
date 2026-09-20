import { NextResponse } from 'next/server';

export async function POST(req) {
  try {
    const { identifier, password } = await req.json();

    if (!identifier || !password) {
      return NextResponse.json({ error: 'Please enter details' }, { status: 400 });
    }

    const mockUser = {
      id: 'usr_123',
      name: identifier.includes('@') ? identifier.split('@')[0] : 'Shoe Enthusiast',
      email: identifier,
    };

    return NextResponse.json({ user: mockUser }, { status: 200 });
  } catch (error) {
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}