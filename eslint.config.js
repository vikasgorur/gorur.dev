const js = require('@eslint/js');
const tseslint = require('@typescript-eslint/eslint-plugin');

module.exports = [
  js.configs.recommended,
  {
    files: ['src/**/*.ts'],
    languageOptions: {
      parser: require('@typescript-eslint/parser'),
      parserOptions: {
        project: './tsconfig.json'
      }
    },
    plugins: {
      '@typescript-eslint': tseslint
    },
    rules: {
      'quotes': ['error', 'double']
    }
  }
]; 