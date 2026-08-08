import * as React from "react";

import { cn } from "@/lib/utils";

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          "flex min-h-[80px] w-full rounded-lg border border-[rgba(0,229,255,0.12)] bg-[rgba(0,0,10,0.4)] px-3 py-2 text-sm text-[#e8e8ff] placeholder:text-[#555577] ring-offset-background transition-all duration-300 focus-visible:outline-none focus-visible:border-neon-cyan focus-visible:ring-1 focus-visible:ring-neon-cyan focus-visible:shadow-neon-cyan-sm disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);
Textarea.displayName = "Textarea";

export { Textarea };
