import * as AccordionPrimitive from "@radix-ui/react-accordion";
import React from "react";
export const Accordion = AccordionPrimitive.Root;
export const AccordionItem = AccordionPrimitive.Item;
export const AccordionTrigger = React.forwardRef(({ children, ...props }, ref) => (
  <AccordionPrimitive.Trigger ref={ref} className="flex w-full justify-between py-2 font-medium" {...props}>
    {children}
  </AccordionPrimitive.Trigger>
));
export const AccordionContent = React.forwardRef(({ children, ...props }, ref) => (
  <AccordionPrimitive.Content ref={ref} className="pb-2 text-sm" {...props}>
    {children}
  </AccordionPrimitive.Content>
));