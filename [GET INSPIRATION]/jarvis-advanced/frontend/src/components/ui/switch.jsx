import * as SwitchPrimitive from "@radix-ui/react-switch";
import React from "react";
export const Switch = React.forwardRef(({ className = "", ...props }, ref) => (
  <SwitchPrimitive.Root ref={ref} className={`h-6 w-10 rounded-full bg-muted data-[state=checked]:bg-primary transition ${className}`} {...props}>
    <SwitchPrimitive.Thumb className="block h-5 w-5 translate-x-[2px] rounded-full bg-background shadow transition data-[state=checked]:translate-x-[22px]" />
  </SwitchPrimitive.Root>
));