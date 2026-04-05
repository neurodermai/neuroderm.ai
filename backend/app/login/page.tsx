'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Sparkles, Eye, EyeOff, ArrowLeft } from 'lucide-react'
import { login, register } from '@/lib/api'
import { useToast } from '@/hooks/use-toast'

export default function LoginPage() {
  const [isLogin, setIsLogin] = useState(true)
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    fullName: '',
    skinType: 'normal'
  })
  
  const router = useRouter()
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      if (isLogin) {
        await login(formData.email, formData.password)
        toast({
          title: "Welcome back! 👋",
          description: "Successfully logged in!",
        })
      } else {
        await register({
          email: formData.email,
          password: formData.password,
          full_name: formData.fullName,
          skin_type: formData.skinType
        })
        toast({
          title: "Account created! 🎉",
          description: "Welcome to NeuroDerm.AI!",
        })
      }
      router.push('/dashboard')
    } catch (error: any) {
      toast({
        title: "Oops! 😅",
        description: error.response?.data?.detail || "Something went wrong",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Back Button */}
        <Link href="/" className="flex items-center gap-2 mb-6 text-gray-600 hover:text-gray-900">
          <ArrowLeft className="h-4 w-4" />
          Back to Home
        </Link>

        <Card className="shadow-xl">
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              <div className="bg-primary/10 p-3 rounded-full">
                <Sparkles className="h-8 w-8 text-primary" />
              </div>
            </div>
            <CardTitle className="text-2xl">
              {isLogin ? 'Welcome Back! 👋' : 'Join Us! 🌟'}
            </CardTitle>
            <CardDescription>
              {isLogin 
                ? 'Sign in to continue your skin health journey' 
                : 'Create an account to track your skin health'}
            </CardDescription>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Full Name (Register only) */}
              {!isLogin && (
                <div>
                  <label className="block text-sm font-medium mb-1">Full Name</label>
                  <input
                    type="text"
                    placeholder="Your name"
                    className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    value={formData.fullName}
                    onChange={(e) => setFormData({...formData, fullName: e.target.value})}
                    required={!isLogin}
                  />
                </div>
              )}

              {/* Email */}
              <div>
                <label className="block text-sm font-medium mb-1">Email</label>
                <input
                  type="email"
                  placeholder="you@example.com"
                  className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  required
                />
              </div>

              {/* Password */}
              <div>
                <label className="block text-sm font-medium mb-1">Password</label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent pr-10"
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    required
                    minLength={8}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400"
                  >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </div>

              {/* Skin Type (Register only) */}
              {!isLogin && (
                <div>
                  <label className="block text-sm font-medium mb-1">Skin Type</label>
                  <select
                    className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    value={formData.skinType}
                    onChange={(e) => setFormData({...formData, skinType: e.target.value})}
                  >
                    <option value="normal">Normal 😊</option>
                    <option value="oily">Oily 💧</option>
                    <option value="dry">Dry 🏜️</option>
                    <option value="combination">Combination 🔄</option>
                    <option value="sensitive">Sensitive 🌸</option>
                  </select>
                </div>
              )}

              {/* Submit Button */}
              <Button type="submit" className="w-full" size="lg" disabled={isLoading}>
                {isLoading ? (
                  <span className="flex items-center gap-2">
                    <div className="spinner h-4 w-4"></div>
                    {isLogin ? 'Signing in...' : 'Creating account...'}
                  </span>
                ) : (
                  isLogin ? 'Sign In 🚀' : 'Create Account ✨'
                )}
              </Button>
            </form>

            {/* Toggle Login/Register */}
            <div className="mt-6 text-center">
              <p className="text-gray-600">
                {isLogin ? "Don't have an account?" : "Already have an account?"}
              </p>
              <button
                onClick={() => setIsLogin(!isLogin)}
                className="text-primary font-semibold hover:underline mt-1"
              >
                {isLogin ? 'Create one here! 🌟' : 'Sign in here! 👋'}
              </button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}