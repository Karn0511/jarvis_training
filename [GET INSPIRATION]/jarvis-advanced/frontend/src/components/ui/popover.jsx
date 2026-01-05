import * as PopoverPrimitive from "@radix-ui/react-popover";
import React from "react";
export const Popover = PopoverPrimitive.Root;
export const PopoverTrigger = PopoverPrimitive.Trigger;
export const PopoverContent = React.forwardRef(({ children, ...props }, ref) => (
  <PopoverPrimitive.Content ref={ref} className="rounded-md border bg-background p-3 text-sm shadow" {...props}>{children}</PopoverPrimitive.Content>
));