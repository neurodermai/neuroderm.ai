import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | Date): string {
  const d = new Date(date)
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

export function formatDateTime(date: string | Date): string {
  const d = new Date(date)
  return d.toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function getHealthScoreColor(score: number): string {
  if (score >= 80) return 'text-green-600'
  if (score >= 60) return 'text-yellow-600'
  if (score >= 40) return 'text-orange-600'
  return 'text-red-600'
}

export function getHealthScoreGradient(score: number): string {
  if (score >= 80) return 'from-green-500 to-emerald-600'
  if (score >= 60) return 'from-yellow-500 to-orange-500'
  if (score >= 40) return 'from-orange-500 to-red-500'
  return 'from-red-500 to-rose-600'
}

export function getSeverityColor(severity: string): string {
  switch (severity.toLowerCase()) {
    case 'minimal':
      return 'bg-green-100 text-green-800'
    case 'mild':
      return 'bg-yellow-100 text-yellow-800'
    case 'moderate':
      return 'bg-orange-100 text-orange-800'
    case 'severe':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

export function formatConditionName(condition: string): string {
  return condition
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}