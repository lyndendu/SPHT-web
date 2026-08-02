import js from "@eslint/js";
import tseslint from "typescript-eslint";

const baseConfig = [
  {
    ignores: ["dist/**", "node_modules/**", ".turbo/**"],
  },
  js.configs.recommended,
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        ecmaFeatures: { jsx: true },
      },
    },
    rules: {
      "no-undef": "off",
      "no-unused-vars": "off",
    },
  },
];

export default baseConfig;
