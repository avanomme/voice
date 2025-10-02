import js from '@eslint/js';
import tsPlugin from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import htmlPlugin from 'eslint-plugin-html';

export default [
  // Base recommended JS rules
  js.configs.recommended,

  // Apply TypeScript parser and plugin
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: tsParser,
      ecmaVersion: 2022,
      sourceType: 'module'
    },
    plugins: {
      '@typescript-eslint': tsPlugin
    },
    rules: {
      ...tsPlugin.configs.recommended.rules
      // add your TS rules overrides here
    }
  },

  // Lint inline JS in HTML
  {
    files: ['**/*.html'],
    plugins: {
      html: htmlPlugin
    },
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module'
    },
    rules: {
      // Add JS rules you want for inline <script> blocks here
    }
  },

  // Common overrides for JS/TS
  {
    rules: {
      'no-unused-vars': 'warn',
      'semi': ['error', 'always']
      // Add any other project-wide rules here
    }
  }
];
