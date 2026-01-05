import React from "react";
export const Skeleton = ({ className = "", ...props }) => (
  <div className={`animate-pulse rounded bg-muted ${className}`} {...props} />
);