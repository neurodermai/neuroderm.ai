'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  Sparkles, 
  TrendingUp, 
  Calendar, 
  Camera, 
  LogOut,
  Heart,
  Star,
  Trophy,
  Target
} from 'lucide-react'
import { getCurrentUser, getHistory, getStats } from '@/lib/api'
import { useToast } from '@/hooks/use-toast'
import { formatDate } from '@/lib/utils'

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null)
  const [history, setHistory] = useState<any[]>([])
  const [stats, setStats] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  
  const router = useRouter()
  const { toast } = useToast()

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const token = localStorage.getItem('token')
      
      if (!token) {
        // Not logged in - show demo data
        setUser({ full_name: 'Guest User', email: 'guest@example.com' })
        setHistory([])
        setStats({ total_analyses: 0, average_health_score: 0, trend: 'no_data' })
        setIsLoading(false)
        return
      }

      const [userData, historyData, statsData] = await Promise.all([
        getCurrentUser().catch(() => null),
        getHistory(5).catch(() => []),
        getStats().catch(() => null)
      ])

      setUser(userData)
      setHistory(historyData)
      setStats(statsData)
    } catch (error) {
      console.error('Failed to load dashboard:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    toast({
      title: "See you soon! 👋",
      description: "You've been logged out successfully",
    })
    router.push('/')
  }

  const getMotivationalMessage = () => {
    const score = stats?.average_health_score || 0
    
    if (score >= 80) {
      return { emoji: '🌟', message: "Your skin is looking AMAZING! Keep up the great work, superstar!" }
    } else if (score >= 60) {
      return { emoji: '💪', message: "You're doing great! A few tweaks and you'll be glowing even more!" }
    } else if (score >= 40) {
      return { emoji: '🌱', message: "Every journey starts somewhere! You're making progress, keep going!" }
    } else {
      return { emoji: '💝', message: "Remember, skin health takes time. We're here to support you every step!" }
    }
  }

  const motivation = getMotivationalMessage()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-primary" />
            <span className="text-xl font-bold gradient-text">NeuroDerm.AI</span>
          </Link>
          
          <div className="flex items-center gap-4">
            <Link href="/analyze">
              <Button>
                <Camera className="h-4 w-4 mr-2" />
                New Analysis
              </Button>
            </Link>
            <Button variant="outline" onClick={handleLogout}>
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">
            Hey {user?.full_name?.split(' ')[0] || 'Friend'}! {motivation.emoji}
          </h1>
          <p className="text-gray-600 text-lg">{motivation.message}</p>
        </div>

        {/* Stats Grid */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-br from-blue-500 to-blue-600 text-white">
            <CardContent className="p-6">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-blue-100 text-sm">Total Analyses</p>
                  <p className="text-3xl font-bold mt-1">{stats?.total_analyses || 0}</p>
                </div>
                <Camera className="h-8 w-8 text-blue-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-500 to-green-600 text-white">
            <CardContent className="p-6">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-green-100 text-sm">Average Score</p>
                  <p className="text-3xl font-bold mt-1">{stats?.average_health_score || 0}</p>
                </div>
                <Heart className="h-8 w-8 text-green-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-purple-500 to-purple-600 text-white">
            <CardContent className="p-6">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-purple-100 text-sm">Trend</p>
                  <p className="text-xl font-bold mt-1 capitalize">
                    {stats?.trend === 'improving' ? '📈 Improving!' : 
                     stats?.trend === 'stable' ? '📊 Stable' : 
                     stats?.trend === 'declining' ? '📉 Needs attention' : '🆕 Start tracking!'}
                  </p>
                </div>
                <TrendingUp className="h-8 w-8 text-purple-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-orange-500 to-orange-600 text-white">
            <CardContent className="p-6">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-orange-100 text-sm">Streak</p>
                  <p className="text-3xl font-bold mt-1">🔥 {history.length || 0}</p>
                </div>
                <Trophy className="h-8 w-8 text-orange-200" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => router.push('/analyze')}>
            <CardContent className="p-6 flex items-center gap-4">
              <div className="bg-primary/10 p-4 rounded-full">
                <Camera className="h-8 w-8 text-primary" />
              </div>
              <div>
                <h3 className="font-semibold text-lg">Analyze Your Skin</h3>
                <p className="text-gray-600">Take a new photo and get instant analysis</p>
              </div>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => router.push('/chat')}>
            <CardContent className="p-6 flex items-center gap-4">
              <div className="bg-green-100 p-4 rounded-full">
                <Sparkles className="h-8 w-8 text-green-600" />
              </div>
              <div>
                <h3 className="font-semibold text-lg">Talk to AI Friend</h3>
                <p className="text-gray-600">Get personalized advice and support</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent History */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              Recent Analyses
            </CardTitle>
            <CardDescription>Your skin health journey</CardDescription>
          </CardHeader>
          <CardContent>
            {history.length > 0 ? (
              <div className="space-y-4">
                {history.map((analysis: any, index: number) => (
                  <div 
                    key={analysis.id || index}
                    className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
                    onClick={() => router.push(`/results/${analysis.id}`)}
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-gray-200 rounded-full overflow-hidden">
                        {analysis.image_url && (
                          <img 
                            src={analysis.image_url} 
                            alt="Analysis" 
                            className="w-full h-full object-cover"
                          />
                        )}
                      </div>
                      <div>
                        <p className="font-medium">
                          Score: {analysis.overall_score}/100
                          {analysis.overall_score >= 80 ? ' 🌟' : 
                           analysis.overall_score >= 60 ? ' 💪' : 
                           analysis.overall_score >= 40 ? ' 🌱' : ' 💝'}
                        </p>
                        <p className="text-sm text-gray-500">
                          {formatDate(analysis.analysis_date)}
                        </p>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      {analysis.primary_concerns?.slice(0, 2).map((concern: string, i: number) => (
                        <span key={i} className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full">
                          {concern}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <Target className="h-12 w-12 mx-auto text-gray-300 mb-4" />
                <h3 className="font-semibold text-lg mb-2">No analyses yet!</h3>
                <p className="text-gray-600 mb-4">Start your skin health journey today</p>
                <Link href="/analyze">
                  <Button>
                    <Camera className="h-4 w-4 mr-2" />
                    Take First Analysis
                  </Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  )
}