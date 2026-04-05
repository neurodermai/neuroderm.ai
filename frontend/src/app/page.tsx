import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { 
  Leaf, 
  Droplets, 
  Sun, 
  Moon, 
  Heart,
  Sparkles,
  ArrowRight,
  Camera,
  MessageCircle,
  TrendingUp
} from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-peaceful">
      {/* Floating Decorations */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-20 left-10 text-6xl opacity-10 animate-float">🌿</div>
        <div className="absolute top-40 right-20 text-5xl opacity-10 animate-float" style={{animationDelay: '1s'}}>🍃</div>
        <div className="absolute bottom-40 left-20 text-4xl opacity-10 animate-float" style={{animationDelay: '2s'}}>🌸</div>
        <div className="absolute bottom-20 right-10 text-5xl opacity-10 animate-float" style={{animationDelay: '0.5s'}}>💧</div>
        <div className="absolute top-1/2 left-1/4 text-3xl opacity-5 animate-breathe">✨</div>
        <div className="absolute top-1/3 right-1/3 text-3xl opacity-5 animate-breathe" style={{animationDelay: '2s'}}>🌙</div>
      </div>

      {/* Header */}
      <header className="sticky top-0 z-50 glass border-b border-sage-200/50">
        <div className="container mx-auto px-6 py-4">
          <nav className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3">
              <div className="w-10 h-10 bg-sage-100 rounded-full flex items-center justify-center">
                <Leaf className="h-5 w-5 text-sage-600" />
              </div>
              <span className="text-xl font-display font-semibold text-sage-800">
                NeuroDerm
                <span className="text-sage-500">.ai</span>
              </span>
            </Link>
            
            <div className="hidden md:flex items-center gap-8">
              <Link href="#features" className="text-sage-600 hover:text-sage-800 transition-colors">
                Features
              </Link>
              <Link href="#journey" className="text-sage-600 hover:text-sage-800 transition-colors">
                Your Journey
              </Link>
              <Link href="/analyze">
                <Button className="btn-peaceful">
                  Start Your Journey
                </Button>
              </Link>
            </div>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto text-center">
            {/* Breathing Circle */}
            <div className="flex justify-center mb-8">
              <div className="relative">
                <div className="w-20 h-20 bg-sage-200/50 rounded-full animate-breathe absolute inset-0"></div>
                <div className="w-20 h-20 bg-sage-100 rounded-full flex items-center justify-center relative">
                  <Sparkles className="h-8 w-8 text-sage-600" />
                </div>
              </div>
            </div>
            
            <h1 className="font-display text-5xl md:text-7xl font-semibold text-sage-800 mb-6 fade-in">
              Your Peaceful
              <span className="block text-gradient-nature">Skin Journey</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-sage-600 mb-4 max-w-2xl mx-auto fade-in stagger-1 leading-relaxed">
              Breathe. Relax. Let AI guide you gently towards healthier, 
              happier skin — at your own pace.
            </p>
            
            <p className="text-sage-500 mb-10 fade-in stagger-2">
              🌿 Gentle Analysis • 💝 Emotional Support • 🧘 Mindful Skincare
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center fade-in stagger-3">
              <Link href="/analyze">
                <button className="btn-peaceful inline-flex items-center gap-2 text-lg">
                  <Camera className="h-5 w-5" />
                  Begin Your Journey
                  <ArrowRight className="h-5 w-5" />
                </button>
              </Link>
              <Link href="/chat">
                <button className="btn-outline-peaceful inline-flex items-center gap-2 text-lg">
                  <MessageCircle className="h-5 w-5" />
                  Talk to AI Friend
                </button>
              </Link>
            </div>
          </div>
        </div>
        
        {/* Wave Divider */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 120" className="w-full h-auto">
            <path 
              fill="rgba(227, 231, 227, 0.5)" 
              d="M0,64L48,69.3C96,75,192,85,288,80C384,75,480,53,576,48C672,43,768,53,864,64C960,75,1056,85,1152,80C1248,75,1344,53,1392,42.7L1440,32L1440,120L1392,120C1344,120,1248,120,1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z"
            />
          </svg>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-sage-50/50">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="font-display text-4xl md:text-5xl font-semibold text-sage-800 mb-4">
              Nurturing Your Skin, Gently
            </h2>
            <p className="text-sage-600 text-lg max-w-2xl mx-auto">
              No pressure. No judgement. Just gentle guidance on your unique skin journey.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <FeatureCard
              icon={<Droplets className="h-8 w-8" />}
              title="Gentle Analysis"
              description="Our AI softly examines your skin, providing insights without harsh judgments"
              color="sky"
            />
            <FeatureCard
              icon={<Heart className="h-8 w-8" />}
              title="Emotional Support"
              description="More than skincare — we care about your wellbeing and feelings too"
              color="lavender"
            />
            <FeatureCard
              icon={<Sun className="h-8 w-8" />}
              title="Daily Rituals"
              description="Transform your routine into peaceful, mindful self-care moments"
              color="sand"
            />
            <FeatureCard
              icon={<Moon className="h-8 w-8" />}
              title="Patient Progress"
              description="Track your journey at your own pace. Small steps, beautiful results"
              color="sage"
            />
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="journey" className="py-24 bg-white/50">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="font-display text-4xl md:text-5xl font-semibold text-sage-800 mb-4">
              Your Gentle Journey
            </h2>
            <p className="text-sage-600 text-lg">
              Three peaceful steps towards understanding your skin better
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <div className="grid md:grid-cols-3 gap-12">
              <JourneyStep
                step="1"
                emoji="📸"
                title="Capture"
                description="Take a calm moment to photograph your skin in natural light"
              />
              <JourneyStep
                step="2"
                emoji="🔮"
                title="Discover"
                description="Our gentle AI reveals insights about your unique skin story"
              />
              <JourneyStep
                step="3"
                emoji="🌱"
                title="Nurture"
                description="Receive personalized, pressure-free guidance to help you bloom"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Testimonial/Quote Section */}
      <section className="py-24 bg-nature">
        <div className="container mx-auto px-6">
          <div className="max-w-3xl mx-auto text-center">
            <div className="text-6xl mb-6">🌸</div>
            <blockquote className="font-display text-3xl md:text-4xl text-sage-800 italic mb-6">
              &ldquo;Take care of your skin like you would tend to a garden — 
              with patience, gentleness, and love.&rdquo;
            </blockquote>
            <p className="text-sage-600">— NeuroDerm Philosophy</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-sage-600">
        <div className="container mx-auto px-6 text-center">
          <div className="max-w-2xl mx-auto">
            <h2 className="font-display text-4xl md:text-5xl font-semibold text-white mb-6">
              Ready to Begin?
            </h2>
            <p className="text-sage-100 text-xl mb-8">
              Your skin journey is unique. Let us walk alongside you, 
              one gentle step at a time.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/analyze">
                <button className="bg-white text-sage-700 px-8 py-4 rounded-full font-medium text-lg hover:bg-sage-50 transition-all shadow-lg">
                  🌿 Start Free Analysis
                </button>
              </Link>
              <Link href="/chat">
                <button className="bg-sage-500 text-white px-8 py-4 rounded-full font-medium text-lg hover:bg-sage-400 transition-all border-2 border-sage-400">
                  💬 Chat with AI Friend
                </button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-sage-800 text-sage-200 py-16">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-12">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-sage-700 rounded-full flex items-center justify-center">
                  <Leaf className="h-5 w-5 text-sage-300" />
                </div>
                <span className="text-xl font-display font-semibold text-white">
                  NeuroDerm.ai
                </span>
              </div>
              <p className="text-sage-400 text-sm">
                Your peaceful companion for mindful skincare. 
                Gentle AI that truly cares.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold text-white mb-4">Explore</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/analyze" className="hover:text-white transition-colors">Skin Analysis</Link></li>
                <li><Link href="/chat" className="hover:text-white transition-colors">AI Friend</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold text-white mb-4">Support</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="#" className="hover:text-white transition-colors">Help Center</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Privacy</Link></li>
                <li><Link href="#" className="hover:text-white transition-colors">Terms</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold text-white mb-4">Connect</h4>
              <p className="text-sm text-sage-400 mb-4">
                Join our peaceful community 🌿
              </p>
              <div className="flex gap-3">
                <div className="w-10 h-10 bg-sage-700 rounded-full flex items-center justify-center hover:bg-sage-600 transition-colors cursor-pointer">
                  💚
                </div>
                <div className="w-10 h-10 bg-sage-700 rounded-full flex items-center justify-center hover:bg-sage-600 transition-colors cursor-pointer">
                  🌸
                </div>
                <div className="w-10 h-10 bg-sage-700 rounded-full flex items-center justify-center hover:bg-sage-600 transition-colors cursor-pointer">
                  ✨
                </div>
              </div>
            </div>
          </div>
          
          <div className="border-t border-sage-700 mt-12 pt-8 text-center">
            <p className="text-sage-400 text-sm">
              © 2024 NeuroDerm.AI — Made with 💚 for mindful skincare
            </p>
            <p className="text-sage-500 text-xs mt-2">
              Remember: You are beautiful, inside and out 🌟
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

function FeatureCard({ icon, title, description, color }: { 
  icon: React.ReactNode
  title: string
  description: string
  color: 'sage' | 'sky' | 'lavender' | 'sand'
}) {
  const colorClasses = {
    sage: 'bg-sage-100 text-sage-600',
    sky: 'bg-sky-100 text-sky-600',
    lavender: 'bg-lavender-100 text-lavender-600',
    sand: 'bg-sand-100 text-sand-600',
  }

  return (
    <div className="card-peaceful p-8 text-center group">
      <div className={`w-16 h-16 ${colorClasses[color]} rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform`}>
        {icon}
      </div>
      <h3 className="font-display text-xl font-semibold text-sage-800 mb-3">{title}</h3>
      <p className="text-sage-600 text-sm leading-relaxed">{description}</p>
    </div>
  )
}

function JourneyStep({ step, emoji, title, description }: {
  step: string
  emoji: string
  title: string
  description: string
}) {
  return (
    <div className="text-center group">
      <div className="relative mb-6">
        <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto shadow-lg shadow-sage-200/50 group-hover:shadow-xl group-hover:scale-105 transition-all">
          <span className="text-4xl">{emoji}</span>
        </div>
        <div className="absolute -top-2 -right-2 w-8 h-8 bg-sage-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
          {step}
        </div>
      </div>
      <h3 className="font-display text-2xl font-semibold text-sage-800 mb-2">{title}</h3>
      <p className="text-sage-600">{description}</p>
    </div>
  )
}