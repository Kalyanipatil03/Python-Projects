import { WishlistProvider } from '../context/context';

export const metadata = {
  title: 'Footwear Store',
  description: 'Flipkart Style Footwear Store',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: 'sans-serif' }}>
        <WishlistProvider>
          {children}
        </WishlistProvider>
      </body>
    </html>
  );
}