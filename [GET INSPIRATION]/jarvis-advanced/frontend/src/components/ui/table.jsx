import React from "react";
export const Table = ({ children, className="" }) => (
  <table className={`w-full text-sm ${className}`}>{children}</table>
);
export const THead = ({ children }) => <thead className="border-b bg-muted/40">{children}</thead>;
export const TBody = ({ children }) => <tbody>{children}</tbody>;
export const TR = ({ children }) => <tr className="border-b last:border-0">{children}</tr>;
export const TH = ({ children }) => <th className="px-3 py-2 text-left font-medium">{children}</th>;
export const TD = ({ children }) => <td className="px-3 py-2">{children}</td>;