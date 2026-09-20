import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  await prisma.shoe.deleteMany({});

  await prisma.shoe.createMany({
    data: [
      {
        name: 'Air Max Pulse',
        brand: 'Nike',
        price: 150.00,
        description: 'An iconic silhouette with modern cushioning for all-day comfort.',
        image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&q=80',
        category: 'Running',
      },
      {
        name: 'Ultraboost Light',
        brand: 'Adidas',
        price: 190.00,
        description: 'Lightweight responsive sneakers engineered for ultimate performance.',
        image: 'https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=600&q=80',
        category: 'Running',
      },
      {
        name: 'Classic Canvas High-Top',
        brand: 'Converse',
        price: 75.00,
        description: 'Timeless high-top sneaker style with durable canvas uppers.',
        image: 'https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=600&q=80',
        category: 'Casual',
      },
      {
        name: 'Retro Runner OG',
        brand: 'Puma',
        price: 110.00,
        description: 'Vintage street style meets modern street comfort.',
        image: 'https://images.unsplash.com/photo-1552346154-21d32810aba3?w=600&q=80',
        category: 'Lifestyle',
      },
    ],
  });

  console.log('Shoe database seeded successfully!');
}

main()
  .catch((e) => console.error(e))
  .finally(async () => await prisma.$disconnect());