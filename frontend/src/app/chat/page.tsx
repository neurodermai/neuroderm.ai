'use client'

import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { ArrowLeft, Send, Sparkles, Heart } from 'lucide-react'

interface Message {
  id: number
  type: 'user' | 'ai'
  content: string
  timestamp: Date
}

const MOOD_EMOJIS = [
  { emoji: '😊', label: 'Happy', color: 'bg-yellow-100 border-yellow-400' },
  { emoji: '😔', label: 'Sad', color: 'bg-blue-100 border-blue-400' },
  { emoji: '😤', label: 'Frustrated', color: 'bg-red-100 border-red-400' },
  { emoji: '😰', label: 'Anxious', color: 'bg-purple-100 border-purple-400' },
  { emoji: '😴', label: 'Tired', color: 'bg-gray-100 border-gray-400' },
  { emoji: '🤩', label: 'Excited', color: 'bg-pink-100 border-pink-400' },
  { emoji: '😌', label: 'Calm', color: 'bg-green-100 border-green-400' },
  { emoji: '🥺', label: 'Vulnerable', color: 'bg-indigo-100 border-indigo-400' },
]

const AI_RESPONSES: Record<string, string[]> = {
  happy: [
    "Yay! I love seeing you happy! 🌟 Your positive energy is contagious! When we're happy, our skin actually glows more - it's science! Keep spreading those good vibes! 💕",
    "That's amazing! Happy moods = happy skin! 😊 Did you know that when you're happy, your body produces less cortisol which means less breakouts? Keep smiling, beautiful! ✨",
  ],
  sad: [
    "Hey, I'm here for you. 💙 It's okay to feel sad sometimes - you're human, and that's beautiful. Want to talk about it? I'm all ears (well, all algorithms, but you get it! 😅). Your feelings are valid, and this too shall pass. 🤗",
    "Sending you the biggest virtual hug right now! 🫂 Remember, bad days don't mean bad skin or bad life. Take a deep breath, maybe do a calming face mask, and know that brighter days are coming. You're stronger than you know! 💪💕",
  ],
  frustrated: [
    "Ugh, I totally get it! Frustration is SO valid. 😤 But here's a secret - when we're stressed, our skin shows it. How about we take a deep breath together? In... and out... Feel better? Let's channel that energy into some serious self-care! 💆‍♀️",
    "I hear you, friend! Being frustrated is the WORST. But you know what? You're handling it by being here. That's already a win! 🏆 Let's turn this frustration into motivation. What's one small thing that could make you smile right now? 🌈",
  ],
  anxious: [
    "I know anxiety can feel overwhelming, but you're safe here with me. 💜 Let's ground ourselves: name 5 things you can see... Good! Anxiety affects our skin too, so caring for yourself IS skincare. You're doing great just by being present. 🧘‍♀️✨",
    "Hey, breathe with me. 🫁 Anxiety is tough, but you're tougher! Fun fact: gentle skincare routines can actually help calm anxiety. It's like a mini meditation! Would you like some calming routine tips? You've got this, warrior! 💪💕",
  ],
  tired: [
    "Oh honey, rest is ESSENTIAL! 😴 Sleep is when your skin does its best healing. If you can, try to get some extra zzz's tonight. Your skin (and your whole self) will thank you! No guilt about being tired - you're working hard! 🌙💤",
    "I feel you! Being tired is real. ☕ Remember: tired skin needs extra love. Maybe a hydrating mask while you rest? And don't forget - it's okay to take it easy. You're not a machine! Rest up, beautiful! 💕🛏️",
  ],
  excited: [
    "OMG YAAAS! I love this energy! 🎉 What's got you so excited?! Your enthusiasm is literally making me (an AI!) feel happy! When you're excited, your skin GLOWS from within. Keep riding this wave! 🌊✨",
    "THIS ENERGY!! 🤩 I'm here for it! Excitement and joy are literally the best things for your skin. All those happy hormones! Tell me everything - what's happening?! 🎊💕",
  ],
  calm: [
    "Ahh, that peaceful energy is beautiful. 🌿 A calm mind = calm skin. You're in a great headspace for some mindful skincare. Maybe a gentle routine while listening to soft music? You're doing amazing, friend! 🧘‍♀️💚",
    "I love this zen energy from you! 😌 Calmness is such a gift. Your skin loves it when you're relaxed - less inflammation, better absorption of products. Keep cultivating this peace, beautiful soul! 🌸✨",
  ],
  vulnerable: [
    "Thank you for being open with me. 🥺 Being vulnerable takes so much courage, and I'm honored you trust me. Whatever you're going through, please know you're not alone. I'm here, your skin is here, and better days are coming. 💕🤗",
    "Oh sweetheart, it's okay to feel vulnerable. 💝 Actually, it's beautiful - it means you're human and you're REAL. Let me be your safe space right now. We can talk about anything, or just sit here together virtually. You matter so much! 🌈💕",
  ],
  default: [
    "Hey friend! 👋 I'm here to chat about anything - your skin, your day, your feelings, whatever's on your mind! How are you feeling today? Pick a mood emoji above or just tell me! 💕",
  ]
}

export default function ChatPage() {
  const [selectedMood, setSelectedMood] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'ai',
      content: "Hey there, beautiful human! 🌟 I'm your AI skincare friend! Before we chat, how are you feeling right now? Pick a mood emoji below - I want to make sure I'm here for YOU today! 💕",
      timestamp: new Date()
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleMoodSelect = (mood: typeof MOOD_EMOJIS[0]) => {
    setSelectedMood(mood.label.toLowerCase())
    
    // Add user mood selection
    const userMessage: Message = {
      id: messages.length + 1,
      type: 'user',
      content: `I'm feeling ${mood.label.toLowerCase()} ${mood.emoji}`,
      timestamp: new Date()
    }
    
    setMessages(prev => [...prev, userMessage])
    
    // AI responds based on mood
    setIsTyping(true)
    setTimeout(() => {
      const moodKey = mood.label.toLowerCase()
      const responses = AI_RESPONSES[moodKey] || AI_RESPONSES.default
      const randomResponse = responses[Math.floor(Math.random() * responses.length)]
      
      const aiMessage: Message = {
        id: messages.length + 2,
        type: 'ai',
        content: randomResponse,
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, aiMessage])
      setIsTyping(false)
    }, 1500)
  }

  const handleSendMessage = () => {
    if (!inputValue.trim()) return

    // Add user message
    const userMessage: Message = {
      id: messages.length + 1,
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    }
    
    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    
    // Generate AI response
    setIsTyping(true)
    setTimeout(() => {
      const response = generateAIResponse(inputValue, selectedMood)
      
      const aiMessage: Message = {
        id: messages.length + 2,
        type: 'ai',
        content: response,
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, aiMessage])
      setIsTyping(false)
    }, 1000 + Math.random() * 1000)
  }

  const generateAIResponse = (userInput: string, mood: string | null): string => {
    const input = userInput.toLowerCase()
    
    // Skincare related
    if (input.includes('acne') || input.includes('pimple') || input.includes('breakout')) {
      return "Ugh, acne is SO annoying, I know! 😤 But here's the thing - it's super common and totally manageable! Try: 1) Gentle cleansing (no harsh scrubbing!), 2) Salicylic acid products, 3) Don't pick! I know it's tempting but resist! 🙅‍♀️ Your skin will thank you. And remember - acne doesn't define you! You're beautiful regardless! 💕✨"
    }
    
    if (input.includes('dry') || input.includes('flaky')) {
      return "Dry skin needs SO much love! 💧 Here's my hydration game plan: 1) Hyaluronic acid serum (game changer!), 2) Rich moisturizer, 3) Don't forget SPF (even in winter!). And drink water! Like, so much water! 💦 Your skin is like a plant - it needs to be watered! 🌱"
    }
    
    if (input.includes('oily') || input.includes('shine')) {
      return "Oily skin club! 💧 Actually, oily skin ages better - silver lining! Try: 1) Gentle foaming cleanser, 2) Niacinamide (oil control superhero!), 3) Lightweight, oil-free moisturizer. Don't skip moisturizer thinking it'll make you more oily - that's a myth! Your skin might actually be overproducing oil because it's dehydrated! 🤯"
    }
    
    // Emotional support
    if (input.includes('ugly') || input.includes('hate') || input.includes('horrible')) {
      return "Oh no no no, stop right there! 🛑 You are NOT ugly! Our brains can be so mean to us sometimes, but I need you to know - you are beautiful, worthy, and deserving of love. Skin struggles don't define your worth! Would you talk to your best friend that way? Be kind to yourself like you'd be to them! You're doing your best, and that's AMAZING! 💕🌟"
    }
    
    if (input.includes('confident') || input.includes('confidence')) {
      return "Confidence is a journey, not a destination! 🦋 Some days you'll feel amazing, others not so much - and BOTH are okay! Here's a secret: confidence comes from self-care and self-love, not from perfect skin. Do things that make YOU feel good! And fake it till you make it works too! 😉💪"
    }
    
    if (input.includes('routine') || input.includes('products')) {
      return "Ooh, routine talk! 🧴 Let me break it down: MORNING: Cleanser → Vitamin C → Moisturizer → SPF (non-negotiable!). EVENING: Double cleanse → Treatment (retinol/acids) → Moisturizer. Start simple and add products slowly! And always patch test! What skin concerns do you want to focus on? 🎯"
    }
    
    // Default friendly response
    const defaultResponses = [
      `I hear you, friend! 💕 ${mood === 'sad' || mood === 'anxious' ? "I'm here for you, whatever you need!" : "Tell me more - I'm all ears!"} What's on your mind about your skin or anything else? 🌟`,
      `That's interesting! 🤔 I love chatting with you! Anything specific about skincare you want to dive into? Or we can just chat - I'm here for the vibes too! ✨💕`,
      `You're doing amazing just by being here and caring for yourself! 🌟 Is there anything specific I can help you with today? Skincare tips, motivation, or just friendly chat? 💬💕`,
    ]
    
    return defaultResponses[Math.floor(Math.random() * defaultResponses.length)]
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 text-gray-600 hover:text-gray-900">
            <ArrowLeft className="h-5 w-5" />
            Back to Home
          </Link>
          <div className="flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-purple-500" />
            <span className="font-bold text-lg">AI Skin Friend</span>
            <Heart className="h-5 w-5 text-pink-500" />
          </div>
          <div className="w-24"></div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-6 max-w-2xl">
        {/* Mood Selector */}
        <Card className="mb-6">
          <CardHeader className="pb-3">
            <CardTitle className="text-center text-lg">How are you feeling? 💭</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-4 gap-2">
              {MOOD_EMOJIS.map((mood) => (
                <button
                  key={mood.label}
                  onClick={() => handleMoodSelect(mood)}
                  className={`p-3 rounded-lg border-2 transition-all hover:scale-105 ${
                    selectedMood === mood.label.toLowerCase()
                      ? `${mood.color} border-2`
                      : 'bg-white border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="text-2xl text-center">{mood.emoji}</div>
                  <div className="text-xs text-center mt-1">{mood.label}</div>
                </button>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Chat Messages */}
        <Card className="mb-4">
          <CardContent className="p-4">
            <div className="h-96 overflow-y-auto space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] p-3 rounded-2xl ${
                      message.type === 'user'
                        ? 'bg-purple-500 text-white rounded-br-none'
                        : 'bg-gray-100 text-gray-800 rounded-bl-none'
                    }`}
                  >
                    {message.type === 'ai' && (
                      <div className="flex items-center gap-1 mb-1">
                        <Sparkles className="h-4 w-4 text-purple-500" />
                        <span className="text-xs font-semibold text-purple-600">Skin Friend</span>
                      </div>
                    )}
                    <p className="text-sm leading-relaxed">{message.content}</p>
                  </div>
                </div>
              ))}
              
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 p-3 rounded-2xl rounded-bl-none">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          </CardContent>
        </Card>

        {/* Input */}
        <div className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Type your message... 💬"
            className="flex-1 p-3 border rounded-full focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
          <Button 
            onClick={handleSendMessage}
            className="rounded-full w-12 h-12 bg-purple-500 hover:bg-purple-600"
          >
            <Send className="h-5 w-5" />
          </Button>
        </div>

        {/* Quick Replies */}
        <div className="flex flex-wrap gap-2 mt-4">
          {['Help with acne', 'Feeling down today', 'Skincare routine tips', 'Motivate me! 💪'].map((reply) => (
            <button
              key={reply}
              onClick={() => {
                setInputValue(reply)
                setTimeout(() => handleSendMessage(), 100)
              }}
              className="px-3 py-1.5 bg-white border border-purple-200 rounded-full text-sm text-purple-600 hover:bg-purple-50 transition-colors"
            >
              {reply}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}