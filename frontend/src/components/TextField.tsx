import React, { useState, ChangeEvent } from "react";

interface CustomInputProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string; // Optional: Specify the input type (e.g., 'text', 'password', 'email')
  placeholder?: string; // Optional: Placeholder text
}

const TextField: React.FC<CustomInputProps> = ({
  label,
  value,
  onChange,
  type = "text",
  placeholder,
}) => {
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.value);
  };

  return (
    <div>
      <label htmlFor={label}>{label}</label>
      <input
        type={type}
        id={label}
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
      />
    </div>
  );
};

export default TextField;
