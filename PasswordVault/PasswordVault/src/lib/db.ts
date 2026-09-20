import Database from 'better-sqlite3';
import path from 'path';

const dbPath = path.join(process.cwd(), 'dev.db');
const db = new Database(dbPath);

db.exec(`
  CREATE TABLE IF NOT EXISTS Shoe (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT NOT NULL,
    image TEXT NOT NULL,
    category TEXT NOT NULL,
    gender TEXT DEFAULT 'Men',
    color TEXT DEFAULT 'Black',
    rating REAL DEFAULT 4.5,
    isOffer INTEGER DEFAULT 0
  )
`);

export function getShoes() {
  const stmt = db.prepare('SELECT * FROM Shoe');
  return stmt.all();
}

export function seedDatabase() {
  const count = (db.prepare('SELECT count(*) as count FROM Shoe').get() as { count: number }).count;
  
  if (count === 0) {
    const insert = db.prepare(`
      INSERT INTO Shoe (id, name, brand, price, description, image, category, gender, color, rating, isOffer)
      VALUES (@id, @name, @brand, @price, @description, @image, @category, @gender, @color, @rating, @isOffer)
    `);

    const sampleShoes = [
      {
        id: '1',
        name: 'Air Max Pulse',
        brand: 'Nike',
        price: 150.00,
        description: 'Iconic running shoes with maximum air cushioning.',
        image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80',
        category: 'Running',
        gender: 'Men',
        color: 'Red',
        rating: 4.8,
        isOffer: 1,
      },
      {
        id: '2',
        name: 'Ultraboost Light',
        brand: 'Adidas',
        price: 190.00,
        description: 'Lightweight high-performance sneakers.',
        image: 'https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=600&q=80',
        category: 'Running',
        gender: 'Women',
        color: 'White',
        rating: 4.6,
        isOffer: 0,
      },
      {
        id: '3',
        name: 'Classic Canvas High-Top',
        brand: 'Converse',
        price: 75.00,
        description: 'Timeless high-top casual street shoes.',
        image: 'https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=600&q=80',
        category: 'Casual',
        gender: 'Kids',
        color: 'Black',
        rating: 4.3,
        isOffer: 1,
      },
      {
        id: '4',
        name: 'Retro Runner OG',
        brand: 'Puma',
        price: 110.00,
        description: 'Vintage street style meets day-long comfort.',
        image: 'https://images.unsplash.com/photo-1552346154-21d32810aba3?w=600&q=80',
        category: 'Lifestyle',
        gender: 'Men',
        color: 'Blue',
        rating: 4.5,
        isOffer: 0,
      },
    ];

    for (const shoe of sampleShoes) {
      insert.run(shoe);
    }
  }
}