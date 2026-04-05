import type { Metadata } from 'next'
import { Nunito, Playfair_Display } from 'next/font/google'
import './globals.css'
import { Toaster } from '@/components/ui/toaster'

const nunito = Nunito({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-nunito',
})

const playfair = Playfair_Display({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-playfair',
})

export const metadata: Metadata = {
  title: 'NeuroDerm.AI - Your Peaceful Skin Journey 🌿',
  description: 'A gentle, AI-powered companion for your skin health journey. Discover peace in skincare.',
  keywords: 'skin analysis, peaceful skincare, AI skincare, skin health, mindful beauty',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${nunito.variable} ${playfair.variable}`}>
      <body className="min-h-screen bg-peaceful antialiased">
        {children}
        <Toaster />
      </body>
    </html>
  )
}