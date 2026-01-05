import * as AvatarPrimitive from "@radix-ui/react-avatar";
import React from "react";
export const Avatar = AvatarPrimitive.Root;
export const AvatarImage = AvatarPrimitive.Image;
export const AvatarFallback = React.forwardRef(({ children, ...props }, ref) => (
  <AvatarPrimitive.Fallback ref={ref} className="flex h-8 w-8 items-center justify-center rounded-full bg-muted text-xs" {...props}>{children}</AvatarPrimitive.Fallback>
));