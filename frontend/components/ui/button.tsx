import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-lg text-sm font-medium ring-offset-background transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default:
          "bg-neon-cyan text-[#0a0a0f] font-semibold hover:shadow-neon-cyan hover:brightness-110 active:scale-[0.98]",
        destructive:
          "bg-neon-red text-white font-semibold hover:shadow-neon-red hover:brightness-110 active:scale-[0.98]",
        outline:
          "border border-[rgba(0,229,255,0.25)] bg-transparent text-neon-cyan hover:bg-[rgba(0,229,255,0.08)] hover:border-neon-cyan hover:shadow-neon-cyan-sm",
        secondary:
          "bg-[rgba(177,74,237,0.12)] border border-[rgba(177,74,237,0.2)] text-[#d4b4ff] hover:bg-[rgba(177,74,237,0.2)] hover:shadow-neon-purple",
        ghost:
          "text-[#8888aa] hover:bg-[rgba(0,229,255,0.06)] hover:text-neon-cyan",
        link: "text-neon-cyan underline-offset-4 hover:underline hover:brightness-125",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-lg px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
