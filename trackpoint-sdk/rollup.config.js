import { defineConfig } from 'rollup'
import RollupTsPlugin from '@rollup/plugin-typescript'
import copy from 'rollup-plugin-copy'

export default defineConfig([
    {
        input: 'lib/main.ts',
        output: {
            file: 'dist/esm/h-trackpoint.js',
            format: 'esm'
        },

        plugins: [RollupTsPlugin()]
    },
    {
        input: 'lib/main.ts',
        output: {
            file: 'dist/cjs/h-trackpoint.js',
            format: 'cjs'
        },
        plugins: [RollupTsPlugin()]
    },
    {
        input: 'lib/main.ts',
        output: {
            file: 'dist/umd/h-trackpoint.js',
            name: 'HTrackpoint',
            format: 'umd'
        },
        plugins: [RollupTsPlugin(), copy({
            targets: [
                {
                    src: 'package.json',
                    dest: 'dist',
                    name: 'package.json'
                },
                {
                    src: 'README.md',
                    dest: 'dist',
                    name: 'README.md'
                }
            ]
        })]
    }
]) 