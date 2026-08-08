import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default: "border-transparent bg-neon-cyan/90 text-[#0a0a0f] shadow-neon-cyan-sm",
        secondary: "border-[rgba(0,229,255,0.12)] bg-[rgba(0,229,255,0.08)] text-[#99ccdd]",
        destructive: "border-transparent bg-neon-red/90 text-white shadow-[0_0_8px_rgba(255,23,68,0.3)]",
        outline: "border-[rgba(0,229,255,0.2)] text-[#99ccdd] bg-transparent",
        success: "border-transparent bg-neon-green/90 text-[#0a0a0f] shadow-[0_0_8px_rgba(57,255,20,0.3)]",
        warning: "border-transparent bg-neon-amber/90 text-[#0a0a0f] shadow-[0_0_8px_rgba(255,184,0,0.3)]",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}

export { Badge, badgeVariants };
