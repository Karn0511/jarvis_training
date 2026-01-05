import * as CheckboxPrimitive from "@radix-ui/react-checkbox";
import React from "react";
export const Checkbox = React.forwardRef(({ className="", ...props }, ref) => (
  <CheckboxPrimitive.Root ref={ref} className={`h-5 w-5 rounded border flex items-center justify-center data-[state=checked]:bg-primary text-primary-foreground ${className}`} {...props}>
    <CheckboxPrimitive.Indicator>✓</CheckboxPrimitive.Indicator>
  </CheckboxPrimitive.Root>
));