const prettierrc = require('./.prettierrc.js');

module.exports = {
    env: {
        browser: true,
        commonjs: true,
        es6: true,
        'jest/globals': true,
        node: true,
    },
    extends: [
        'eslint:recommended',
        'plugin:functional/external-typescript-recommended',
        'plugin:import/recommended',
        'plugin:node/recommended',
        'plugin:prettier/recommended',
        'prettier',
    ],
    plugins: [
        '@typescript-eslint',
        'functional',
        'import',
        'jest',
        'json-files',
        'prettier',
        'regex',
    ],
    reportUnusedDisableDirectives: true,
    globals: {
        Atomics: 'readonly',
        SharedArrayBuffer: 'readonly',
    },
    parser: '@typescript-eslint/parser',
    parserOptions: {
        ecmaVersion: 2022,
        project: './tsconfig.json',
        sourceType: 'module',
    },
    root: true,
    rules: {
        eqeqeq: 'warn',
        'import/default': 2,
        'import/export': 2,
        'import/named': 2,
        'import/namespace': 2,
        'import/newline-after-import': 2,
        'import/no-duplicates': 2,
        'import/no-unresolved': [2, { commonjs: true, amd: true }],
        'import/no-useless-path-segments': 'error',
        'import/order': 2,
        'json-files/sort-package-json': 'error',
        'no-console': 'error',
        'no-param-reassign': 'warn',
        'no-restricted-imports': [
            'warn',
            {
                name: '@local/lib/db',
                message:
                    'Knex object as function parameter preferred to direct database import',
            },
            {
                name: 'winston',
                message:
                    'Prefer use of finch logger under @finch-api/common/dist/logger',
            },
            {
                name: 'pino',
                message:
                    'Prefer use of finch logger under @finch-api/common/dist/logger',
            },
            {
                name: 'unleash-client',
                message:
                    'The unleash client should not be used directly instead use @workspace/lib-feature-flags',
            },
            {
                name: 'node-fetch',
                message: "Prefer use of Node's global fetch",
            },
        ],
        'no-unused-vars': [
            'warn',
            { varsIgnorePattern: '^_', argsIgnorePattern: '^_' },
        ],
        'node/no-missing-import': 'off', // conflicts with typescript absolute imports
        'node/no-unpublished-import': [
            'error',
            {
                allowModules: ['type-fest'],
            },
        ],
        'node/no-unsupported-features/es-syntax': 'off',
        'node/shebang': 'off',
        'prettier/prettier': ['error', prettierrc],
        'regex/invalid': [
            'error',
            [
                /**
                 * Forces imports from only top level npm workspace exports.
                 * E.g. '@workspaces/lib-errors/bad-request' -> '@workspaces/lib-errors'
                 */
                {
                    regex: '@workspace/(.+)/(.+)',
                    replacement: {
                        function:
                            "return captured[1].includes(');') ? `@workspace/${captured[0]}');` : `@workspace/${captured[0]}'`;",
                    },
                    message: 'Export public functionality of workspace from index.ts',
                },
                /**
                 * Replace migrated libs to corresponding workspaces
                 */
                {
                    regex:
                        '@local/lib/(errors|feature-flags|format|browser|blog|result|slack|validate|redis|infra-primitives)(.+)',
                    replacement: {
                        function:
                            "return captured[1].includes(');') ? `@workspace/lib-${captured[0]}');` : `@workspace/lib-${captured[0]}'`;",
                    },
                    message: 'Please access via @workspace/lib-<lib>!',
                },
                /**
                 * Replace migrated adapters to corresponding workspaces
                 */
                {
                    regex:
                        '@local/adapters/(types|schema|base|adp-run|adp-totalsource|aspen-hr|bambee|bamboo-hr)(.+)',
                    replacement: {
                        function:
                            "return captured[1].includes(');') ? `@workspace/adapter-${captured[0]}');` : `@workspace/adapter-${captured[0]}'`;",
                    },
                    message: 'Please access via @workspace/adapter-<adapter>!',
                },
            ],
            '.eslintrc.js',
        ],
        '@typescript-eslint/no-floating-promises': [
            'warn',
            { ignoreVoid: true, ignoreIIFE: true },
        ],
        '@typescript-eslint/no-misused-promises': 'warn',
        yoda: 'error',
    },
    settings: {
        'import/parsers': {
            '@typescript-eslint/parser': ['.ts'],
        },
        'import/resolver': {
            node: { extensions: ['.ts', '.js'] },
            typescript: {
                alwaysTryTypes: true,
            },
        },
        node: {
            resolvePaths: ['node_modules/@types'],
            tryExtensions: ['.js', '.json', '.node', '.ts', '.d.ts'],
        },
    },
    overrides: [
        {
            files: ['**/*.ts', '**/*.tsx'],
            extends: [
                'typescript',
                'plugin:@typescript-eslint/recommended',
                'plugin:@typescript-eslint/recommended-requiring-type-checking',
                'plugin:import/typescript',
            ],
            rules: {
                '@typescript-eslint/await-thenable': 'warn',
                '@typescript-eslint/no-explicit-any': 'error',
                '@typescript-eslint/no-floating-promises': 'warn',
                '@typescript-eslint/no-misused-promises': 'warn',
                '@typescript-eslint/no-unsafe-argument': 'warn',
                '@typescript-eslint/no-unsafe-assignment': 'warn',
                '@typescript-eslint/no-unsafe-call': 'warn',
                '@typescript-eslint/no-unsafe-member-access': 'warn',
                '@typescript-eslint/no-unsafe-return': 'warn',
                '@typescript-eslint/no-unused-vars': [
                    'error',
                    { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
                ],
                '@typescript-eslint/require-await': 'warn',
                '@typescript-eslint/restrict-plus-operands': 'warn',
                '@typescript-eslint/restrict-template-expressions': 'warn',
                '@typescript-eslint/unbound-method': 'warn',
                'import/default': 'warn',
                'import/export': 'warn',
                'import/namespace': 'warn',
                'import/newline-after-import': 'warn',
                'import/no-default-export': 'warn',
                'import/no-duplicates': 'warn',
                'import/no-named-as-default': 'error',
                'import/no-namespace': [
                    'warn',
                    {
                        ignore: [
                            // TODO: remove these incrementally, enable for JS files
                            'bluebird',
                            'cheerio',
                            'dotenv',
                            'faker',
                            'joi',
                            'moment',
                            'moment-range',
                            'otplib',
                            'querystring',
                            '@local/**/*',
                        ],
                    },
                ],
                'import/no-relative-packages': 'warn',
            },
        },
        {
            files: [
                'adapters/google-sheets/**',
                'lib/finch-accountant/**',
                'migrations/**',
                'scripts/**',
            ],
            rules: {
                'no-console': 'off',
            },
        },
    ],
};
