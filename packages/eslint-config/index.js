module.exports = {
  parser: require.resolve('@typescript-eslint/parser'),
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: { jsx: true },
  },
  env: { browser: true, node: true, es2022: true },
  extends: ['eslint:recommended'],
  rules: { 'no-undef': 'off', 'no-unused-vars': 'off' },
}
