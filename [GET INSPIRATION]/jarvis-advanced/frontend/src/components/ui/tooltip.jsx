import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import React from "react";
export const TooltipProvider = TooltipPrimitive.Provider;
export const Tooltip = TooltipPrimitive.Root;
export const TooltipTrigger = TooltipPrimitive.Trigger;
export const TooltipContent = React.forwardRef(({ children, ...props }, ref) => (
  <TooltipPrimitive.Content ref={ref} className="rounded bg-muted px-2 py-1 text-xs shadow" {...props}>{children}</TooltipPrimitive.Content>
));