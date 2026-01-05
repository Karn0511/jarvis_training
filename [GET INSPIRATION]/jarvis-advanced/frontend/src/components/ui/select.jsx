import * as SelectPrimitive from "@radix-ui/react-select";
import React from "react";
export const Select = SelectPrimitive.Root;
export const SelectTrigger = React.forwardRef(({ children, ...props }, ref) => (
  <SelectPrimitive.Trigger ref={ref} className="flex h-9 w-full items-center justify-between rounded-md border px-3 text-sm" {...props}>
    <SelectPrimitive.Value>{children}</SelectPrimitive.Value>
    <SelectPrimitive.Icon>▾</SelectPrimitive.Icon>
  </SelectPrimitive.Trigger>
));
export const SelectContent = React.forwardRef(({ children, ...props }, ref) => (
  <SelectPrimitive.Content ref={ref} className="rounded-md border bg-background p-1 shadow" {...props}>
    <SelectPrimitive.Viewport>{children}</SelectPrimitive.Viewport>
  </SelectPrimitive.Content>
));
export const SelectItem = React.forwardRef(({ children, ...props }, ref) => (
  <SelectPrimitive.Item ref={ref} className="cursor-pointer rounded px-2 py-1 text-sm data-[highlighted]:bg-muted" {...props}>
    <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
  </SelectPrimitive.Item>
));