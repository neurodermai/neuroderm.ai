import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-full text-sm font-medium ring-offset-background transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sage-400 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-sage-500 text-white hover:bg-sage-600 shadow-md hover:shadow-lg hover:-translate-y-0.5",
        destructive:
          "bg-red-400 text-white hover:bg-red-500",
        outline:
          "border-2 border-sage-300 bg-white/80 hover:bg-sage-50 text-sage-700",
        secondary:
          "bg-sage-100 text-sage-700 hover:bg-sage-200",
        ghost: "hover:bg-sage-100 text-sage-600",
        link: "text-sage-600 underline-offset-4 hover:underline",
        peaceful: "bg-sage-500 text-white hover:bg-sage-600 shadow-lg shadow-sage-300/30 hover:shadow-xl hover:-translate-y-1",
      },
      size: {
        default: "h-11 px-6 py-2",
        sm: "h-9 rounded-full px-4",
        lg: "h-13 rounded-full px-8 text-base",
        icon: "h-11 w-11",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }