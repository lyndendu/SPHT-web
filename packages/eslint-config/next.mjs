import js from "@eslint/js";
import nextPluginModule from "@next/eslint-plugin-next";
import jsxA11yPluginModule from "eslint-plugin-jsx-a11y";
import reactPluginModule from "eslint-plugin-react";
import reactHooksPluginModule from "eslint-plugin-react-hooks";
import globals from "globals";
import tseslint from "typescript-eslint";

const nextPlugin = nextPluginModule.default ?? nextPluginModule;
const reactPlugin = reactPluginModule.default ?? reactPluginModule;
const reactHooksPlugin = reactHooksPluginModule.default ?? reactHooksPluginModule;
const jsxA11yPlugin = jsxA11yPluginModule.default ?? jsxA11yPluginModule;

const nextConfig = [
  {
    ignores: [".next/**", "out/**", "build/**", "node_modules/**", ".turbo/**"],
  },
  js.configs.recommended,
  {
    files: ["**/*.{js,jsx,ts,tsx}"],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        ecmaFeatures: { jsx: true },
      },
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      "@next/next": nextPlugin,
      react: reactPlugin,
      "react-hooks": reactHooksPlugin,
      "jsx-a11y": jsxA11yPlugin,
    },
    settings: {
      react: { version: "detect" },
    },
    rules: {
      ...nextPlugin.configs.recommended.rules,
      ...nextPlugin.configs["core-web-vitals"].rules,
      ...reactPlugin.configs.recommended.rules,
      ...reactPlugin.configs["jsx-runtime"].rules,
      ...reactHooksPlugin.configs.recommended.rules,
      ...jsxA11yPlugin.configs.recommended.rules,
      "no-undef": "off",
      "no-unused-vars": "off",
      "react/prop-types": "off",
      "react/react-in-jsx-scope": "off",
    },
  },
];

export default nextConfig;
