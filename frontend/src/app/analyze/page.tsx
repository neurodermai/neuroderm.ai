'use client'

import { useState } from 'react'
import ImageUpload from '@/components/ImageUpload'
import AnalysisResults from '@/components/AnalysisResults'
import { ArrowLeft, Leaf, Sparkles } from 'lucide-react'
import Link from 'next/link'
import { analyzeImage } from '@/lib/api'
import { useToast } from '@/hooks/use-toast'

export default function AnalyzePage() {
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const { toast } = useToast()

  const handleImageUpload = async (file: File) => {
    setIsAnalyzing(true)
    
    try {
      const result = await analyzeImage(file)
      setAnalysisResult(result)
      
      toast({
        title: "Analysis Complete 🌿",
        description: "Your gentle skin reading is ready!",
      })
    } catch (error: any) {
      toast({
        title: "Oops, something went wrong",
        description: error.message || "Please try again",
        variant: "destructive",
      })
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleReset = () => {
    setAnalysisResult(null)
  }

  return (
    <div className="min-h-screen bg-peaceful">
      {/* Floating Decorations */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-20 right-10 text-5xl opacity-10 animate-float">🌿</div>
        <div className="absolute bottom-40 left-10 text-4xl opacity-10 animate-float" style={{animationDelay: '1s'}}>🌸</div>
        <div className="absolute top-1/2 right-1/4 text-3xl opacity-5 animate-breathe">✨</div>
      </div>

      {/* Header */}
      <header className="sticky top-0 z-50 glass border-b border-sage-200/50">
        <div className="container mx-auto px-6 py-4">
          <nav className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2 text-sage-600 hover:text-sage-800 transition-colors">
              <ArrowLeft className="h-5 w-5" />
              <span>Back to Home</span>
            </Link>
            
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-sage-100 rounded-full flex items-center justify-center">
                <Leaf className="h-4 w-4 text-sage-600" />
              </div>
              <span className="font-display font-semibold text-sage-800">NeuroDerm.ai</span>
            </div>

            <div className="w-24" />
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-12 relative z-10">
        <div className="max-w-4xl mx-auto">
          {!analysisResult ? (
            <>
              {/* Title Section */}
              <div className="text-center mb-12 fade-in">
                <div className="inline-flex items-center gap-2 bg-sage-100 px-4 py-2 rounded-full mb-6">
                  <Sparkles className="h-4 w-4 text-sage-600" />
                  <span className="text-sage-700 text-sm">Gentle AI Analysis</span>
                </div>
                
                <h1 className="font-display text-4xl md:text-5xl font-semibold text-sage-800 mb-4">
                  Let&apos;s Understand Your Skin
                </h1>
                <p className="text-sage-600 text-lg max-w-xl mx-auto">
                  Take a peaceful moment to capture your skin. 
                  No pressure, no judgement — just gentle insights.
                </p>
              </div>
              
              {/* Upload Component */}
              <div className="fade-in stagger-1">
                <ImageUpload 
                  onUpload={handleImageUpload}
                  isLoading={isAnalyzing}
                />
              </div>
              
              {/* Tips Section */}
              <div className="mt-12 card-peaceful p-8 fade-in stagger-2">
                <h3 className="font-display text-xl font-semibold text-sage-800 mb-4 text-center">
                  🌿 Tips for a Peaceful Photo
                </h3>
                <div className="grid md:grid-cols-3 gap-6">
                  <TipCard
                    emoji="☀️"
                    title="Natural Light"
                    description="Find a calm spot near a window with soft, natural lighting"
                  />
                  <TipCard
                    emoji="😌"
                    title="Bare Skin"
                    description="Gently cleanse your face — no makeup needed here"
                  />
                  <TipCard
                    emoji="🧘"
                    title="Relax"
                    description="Take a deep breath. There's no rush. You're doing great!"
                  />
                </div>
              </div>
            </>
          ) : (
            <AnalysisResults 
              result={analysisResult}
              onReset={handleReset}
            />
          )}
        </div>
      </main>
    </div>
  )
}

function TipCard({ emoji, title, description }: {
  emoji: string
  title: string
  description: string
}) {
  return (
    <div className="text-center">
      <div className="text-3xl mb-2">{emoji}</div>
      <h4 className="font-semibold text-sage-700 mb-1">{title}</h4>
      <p className="text-sage-600 text-sm">{description}</p>
    </div>
  )
}