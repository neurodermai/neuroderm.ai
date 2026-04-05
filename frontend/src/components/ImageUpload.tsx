'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, X, Leaf, Camera } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface ImageUploadProps {
  onUpload: (file: File) => void
  isLoading?: boolean
}

export default function ImageUpload({ onUpload, isLoading = false }: ImageUploadProps) {
  const [preview, setPreview] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      setSelectedFile(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.heic']
    },
    maxFiles: 1,
    disabled: isLoading
  })

  const handleAnalyze = () => {
    if (selectedFile) {
      onUpload(selectedFile)
    }
  }

  const handleReset = () => {
    setPreview(null)
    setSelectedFile(null)
  }

  if (preview && !isLoading) {
    return (
      <div className="max-w-xl mx-auto">
        <div className="card-peaceful overflow-hidden">
          <div className="relative aspect-square">
            <img
              src={preview}
              alt="Preview"
              className="w-full h-full object-cover"
            />
          </div>
          <div className="p-6 bg-white/80">
            <p className="text-center text-sage-600 mb-4">
              ✨ Looking good! Ready when you are.
            </p>
            <div className="flex gap-4">
              <Button
                onClick={handleAnalyze}
                className="flex-1 btn-peaceful"
              >
                <Leaf className="h-5 w-5 mr-2" />
                Begin Gentle Analysis
              </Button>
              <Button
                onClick={handleReset}
                variant="outline"
                className="border-sage-300 text-sage-600 hover:bg-sage-50"
              >
                <X className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="max-w-xl mx-auto">
        <div className="card-peaceful p-12 text-center">
          {/* Breathing Animation */}
          <div className="relative w-24 h-24 mx-auto mb-6">
            <div className="absolute inset-0 bg-sage-200 rounded-full animate-breathe"></div>
            <div className="absolute inset-2 bg-sage-100 rounded-full animate-breathe" style={{animationDelay: '0.5s'}}></div>
            <div className="absolute inset-4 bg-white rounded-full flex items-center justify-center">
              <Leaf className="h-8 w-8 text-sage-500 animate-pulse" />
            </div>
          </div>
          
          <h3 className="font-display text-2xl text-sage-800 mb-2">
            Gently Analyzing...
          </h3>
          <p className="text-sage-600 mb-4">
            Take a deep breath. Your results are being prepared with care.
          </p>
          
          {/* Calming Messages */}
          <div className="text-sage-500 text-sm animate-pulse">
            🌿 Understanding your unique skin story...
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-xl mx-auto">
      <div
        {...getRootProps()}
        className={`
          card-peaceful p-12 text-center cursor-pointer transition-all duration-300
          ${isDragActive 
            ? 'ring-4 ring-sage-300 bg-sage-50' 
            : 'hover:shadow-xl hover:-translate-y-1'
          }
        `}
      >
        <input {...getInputProps()} />
        
        {/* Icon */}
        <div className="relative w-20 h-20 mx-auto mb-6">
          <div className="absolute inset-0 bg-sage-100 rounded-full"></div>
          <div className="absolute inset-0 bg-sage-200/50 rounded-full animate-breathe"></div>
          <div className="relative w-full h-full flex items-center justify-center">
            {isDragActive ? (
              <Leaf className="h-10 w-10 text-sage-600" />
            ) : (
              <Camera className="h-10 w-10 text-sage-500" />
            )}
          </div>
        </div>
        
        <h3 className="font-display text-2xl text-sage-800 mb-2">
          {isDragActive ? 'Drop your photo here 🌸' : 'Share Your Photo'}
        </h3>
        
        <p className="text-sage-600 mb-6">
          Drag & drop or click to select an image of your skin
        </p>
        
        <button className="btn-outline-peaceful inline-flex items-center gap-2">
          <Upload className="h-5 w-5" />
          Choose Photo
        </button>
        
        <p className="text-sage-400 text-sm mt-6">
          JPEG, PNG, or HEIC • Max 10MB
        </p>
      </div>
    </div>
  )
}