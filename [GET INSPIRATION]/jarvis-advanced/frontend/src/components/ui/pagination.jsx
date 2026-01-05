import React from "react";
export const Pagination = ({ page, totalPages, onChange }) => {
  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);
  return (
    <div className="flex gap-1">
      {pages.map(p => (
        <button
          key={p}
          onClick={() => onChange(p)}
          className={`h-8 w-8 rounded text-sm ${p === page ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}
        >{p}</button>
      ))}
    </div>
  );
};