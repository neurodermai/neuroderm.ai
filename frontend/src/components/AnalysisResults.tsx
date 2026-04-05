'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { 
  ArrowLeft, 
  AlertCircle, 
  Info,
  Sparkles,
  TrendingUp,
  Calendar,
  Heart,
  MessageCircle
} from 'lucide-react'
import { 
  getHealthScoreColor, 
  getHealthScoreGradient, 
  getSeverityColor,
  formatConditionName,
  formatDateTime
} from '@/lib/utils'
import Link from 'next/link'

interface AnalysisResultsProps {
  result: any
  onReset: () => void
}

export default function AnalysisResults({ result, onReset }: AnalysisResultsProps) {
  const { results, recommendations, timestamp, image_url } = result
  const [showMotivation, setShowMotivation] = useState(true)

  // Get motivational message based on score
  const getMotivationalContent = () => {
    const score = results.overall_health_score

    if (score >= 80) {
      return {
        emoji: '🌟',
        title: "WOW! You're Absolutely Glowing!",
        message: "Your skin is looking fantastic! Whatever you're doing, KEEP DOING IT! You're a skincare superstar! ⭐",
        tip: "Pro tip: Consistency is your secret weapon. Keep up this amazing routine!",
        color: 'from-green-400 to-emerald-500'
      }
    } else if (score >= 60) {
      return {
        emoji: '💪',
        title: "Great Job, You're On The Right Track!",
        message: "Your skin is doing well! With a few small tweaks, you'll be glowing even more. You've got this! 🎯",
        tip: "Focus on the recommendations below - small changes lead to big results!",
        color: 'from-blue-400 to-cyan-500'
      }
    } else if (score >= 40) {
      return {
        emoji: '🌱',
        title: "Every Journey Starts Somewhere!",
        message: "Hey friend, I see you're working on your skin health - that takes courage! Remember, progress isn't always linear. You're doing amazing just by being here! 💚",
        tip: "Let's tackle one thing at a time. Small steps lead to beautiful skin!",
        color: 'from-yellow-400 to-orange-500'
      }
    } else {
      return {
        emoji: '💝',
        title: "I'm Here For You, Friend!",
        message: "Listen, skin struggles are REAL and you're not alone. The fact that you're here taking action shows how strong you are. We're going to get through this together! 🤗",
        tip: "Don't be too hard on yourself. Skin health is a journey, not a destination. You've got a whole community cheering for you!",
        color: 'from-pink-400 to-rose-500'
      }
    }
  }

  const motivation = getMotivationalContent()

  // Fix image URL - handle different formats
  const getImageUrl = (url: string) => {
    if (!url) return '/placeholder-skin.jpg'
    if (url.startsWith('http')) return url
    if (url.startsWith('/')) return `http://localhost:8000${url}`
    return `http://localhost:8000/${url}`
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <Button onClick={onReset} variant="outline">
          <ArrowLeft className="h-4 w-4 mr-2" />
          New Analysis
        </Button>
        <div className="flex gap-2">
          <Link href="/chat">
            <Button variant="outline">
              <MessageCircle className="h-4 w-4 mr-2" />
              Talk to AI Friend
            </Button>
          </Link>
        </div>
      </div>

      {/* Motivational Message Card */}
      {showMotivation && (
        <Card className={`overflow-hidden bg-gradient-to-r ${motivation.color} text-white`}>
          <CardContent className="p-6">
            <div className="flex justify-between items-start">
              <div>
                <div className="text-4xl mb-2">{motivation.emoji}</div>
                <h2 className="text-2xl font-bold mb-2">{motivation.title}</h2>
                <p className="text-lg opacity-95 mb-3">{motivation.message}</p>
                <p className="text-sm bg-white/20 rounded-lg p-3">
                  💡 {motivation.tip}
                </p>
              </div>
              <button 
                onClick={() => setShowMotivation(false)}
                className="text-white/70 hover:text-white"
              >
                ✕
              </button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Overall Health Score */}
      <Card className="overflow-hidden">
        <div className={`h-2 bg-gradient-to-r ${getHealthScoreGradient(results.overall_health_score)}`} />
        <CardHeader className="text-center">
          <CardTitle className="text-2xl mb-2">Your Skin Health Score</CardTitle>
          <div className={`text-6xl font-bold ${getHealthScoreColor(results.overall_health_score)}`}>
            {results.overall_health_score}
            <span className="text-2xl">/100</span>
          </div>
          <p className="text-gray-600 mt-2">
            {results.overall_health_score >= 80 ? '🏆 Excellent!' : 
             results.overall_health_score >= 60 ? '👍 Good!' : 
             results.overall_health_score >= 40 ? '🌱 Room to grow!' : '💪 Let\'s improve together!'}
          </p>
        </CardHeader>
      </Card>

      {/* Image and Conditions */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Analyzed Image */}
        <Card>
          <CardHeader>
            <CardTitle>Analyzed Image</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="relative aspect-square rounded-lg overflow-hidden bg-gray-100">
              <img
                src={getImageUrl(image_url)}
                alt="Analyzed skin"
                className="w-full h-full object-cover"
                onError={(e) => {
                  const target = e.target as HTMLImageElement
                  target.src = 'https://via.placeholder.com/400x400?text=Your+Image'
                }}
              />
            </div>
            <p className="text-sm text-gray-500 mt-2 text-center">
              📅 {formatDateTime(timestamp)}
            </p>
          </CardContent>
        </Card>

        {/* Detected Conditions */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5" />
              What We Found
            </CardTitle>
            <CardDescription>
              {results.num_conditions_detected === 0 
                ? "No major concerns - you're doing great! 🎉" 
                : `${results.num_conditions_detected} area(s) to focus on`}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {results.detected_conditions.length > 0 ? (
              <div className="space-y-4">
                {results.detected_conditions.map((condition: any, index: number) => (
                  <div key={index} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="font-medium">
                        {formatConditionName(condition.condition)}
                      </span>
                      <Badge className={getSeverityColor(condition.severity)}>
                        {condition.severity}
                      </Badge>
                    </div>
                    <div className="space-y-1">
                      <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">Confidence</span>
                        <span className="font-medium">
                          {Math.round(condition.confidence * 100)}%
                        </span>
                      </div>
                      <Progress value={condition.confidence * 100} />
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="text-5xl mb-3">🎉</div>
                <p className="font-semibold text-lg">Looking Good!</p>
                <p className="text-gray-600">No major skin concerns detected.</p>
                <p className="text-gray-600">Keep up the great work!</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Friend's Advice Section */}
      <Card className="border-2 border-purple-200 bg-purple-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-purple-800">
            <Heart className="h-5 w-5" />
            A Note From Your Skin Friend 💜
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <p className="text-gray-700 leading-relaxed">
              {results.overall_health_score >= 60 ? (
                <>
                  Hey there, gorgeous! 💕 Just wanted to say - you&apos;re doing AMAZING!
                  Your skin is reflecting all the love and care you&apos;re giving it.
                  Remember, true beauty comes from within, and yours is definitely shining through!
                  Keep being your awesome self! 🌟
                </>
              ) : (
                <>
                  Hey friend, I want you to know something important - your worth isn&apos;t
                  determined by your skin! 💝 We ALL have skin struggles at some point.
                  The fact that you&apos;re here, taking action, shows how amazing you are.
                  Let&apos;s work on this together, one step at a time. I believe in you!
                  You&apos;ve got this, and I&apos;ve got your back! 🤗✨
                </>
              )}
            </p>
            <div className="mt-4 flex gap-2">
              <Link href="/chat">
                <Button size="sm" className="bg-purple-600 hover:bg-purple-700">
                  <MessageCircle className="h-4 w-4 mr-2" />
                  Chat More With Me
                </Button>
              </Link>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Your Personalized Plan
          </CardTitle>
          <CardDescription>
            Small changes, big results! Here&apos;s what I recommend:
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="immediate" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="immediate">Quick Wins 🎯</TabsTrigger>
              <TabsTrigger value="routine">Routine 🧴</TabsTrigger>
              <TabsTrigger value="lifestyle">Lifestyle 🌿</TabsTrigger>
            </TabsList>

            <TabsContent value="immediate" className="space-y-4 mt-4">
              {recommendations.immediate_actions.map((action: any, index: number) => (
                <div key={index} className="flex gap-3 p-4 bg-secondary/50 rounded-lg">
                  <div className="flex-shrink-0">
                    <div className={`
                      w-3 h-3 rounded-full mt-1.5
                      ${action.priority === 'high' ? 'bg-red-500' : ''}
                      ${action.priority === 'medium' ? 'bg-yellow-500' : ''}
                      ${action.priority === 'low' ? 'bg-green-500' : ''}
                    `} />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold mb-1">{action.title}</h4>
                    <p className="text-sm text-muted-foreground">{action.description}</p>
                  </div>
                </div>
              ))}
            </TabsContent>

            <TabsContent value="routine" className="space-y-4 mt-4">
              <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                <h4 className="font-semibold mb-3 flex items-center gap-2">
                  ☀️ Morning Routine
                </h4>
                <ol className="space-y-2">
                  {recommendations.skincare_routine.morning.map((step: string, index: number) => (
                    <li key={index} className="flex items-start gap-2 text-sm">
                      <span className="bg-yellow-500 text-white w-5 h-5 rounded-full flex items-center justify-center text-xs flex-shrink-0">
                        {index + 1}
                      </span>
                      <span>{step}</span>
                    </li>
                  ))}
                </ol>
              </div>

              <div className="bg-indigo-50 p-4 rounded-lg border border-indigo-200">
                <h4 className="font-semibold mb-3 flex items-center gap-2">
                  🌙 Evening Routine
                </h4>
                <ol className="space-y-2">
                  {recommendations.skincare_routine.evening.map((step: string, index: number) => (
                    <li key={index} className="flex items-start gap-2 text-sm">
                      <span className="bg-indigo-500 text-white w-5 h-5 rounded-full flex items-center justify-center text-xs flex-shrink-0">
                        {index + 1}
                      </span>
                      <span>{step}</span>
                    </li>
                  ))}
                </ol>
              </div>
            </TabsContent>

            <TabsContent value="lifestyle" className="space-y-4 mt-4">
              {recommendations.lifestyle_tips.map((tip: any, index: number) => (
                <div key={index} className="flex gap-3 p-4 bg-green-50 rounded-lg border border-green-200">
                  <span className="text-2xl">{['🥗', '💧', '😴', '🧘', '🏃'][index % 5]}</span>
                  <div className="flex-1">
                    <h4 className="font-semibold mb-1">{tip.title}</h4>
                    <p className="text-sm text-muted-foreground">{tip.description}</p>
                  </div>
                </div>
              ))}
            </TabsContent>
          </Tabs>

          {/* Product Categories */}
          <div className="mt-6">
            <h4 className="font-semibold mb-3">🛍️ Products To Look For</h4>
            <div className="flex flex-wrap gap-2">
              {recommendations.product_categories.map((category: string, index: number) => (
                <Badge key={index} variant="secondary" className="text-sm">
                  {category}
                </Badge>
              ))}
            </div>
          </div>

          {/* Doctor Recommendation */}
          {recommendations.when_to_see_doctor && (
            <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg flex gap-3">
              <AlertCircle className="h-5 w-5 text-amber-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-amber-900 mb-1">
                  When To See A Professional 👩‍⚕️
                </h4>
                <p className="text-sm text-amber-800">
                  {recommendations.when_to_see_doctor}
                </p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}