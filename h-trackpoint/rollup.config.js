import { defineConfig } from 'rollup'
import RollupTsPlugin from '@rollup/plugin-typescript'
import copy from 'rollup-plugin-copy'
import RollupGeneratePackageJSONPlugin from 'rollup-plugin-generate-package-json'
import packageJSON from './package.json' with  { type: 'json' };
import resolve from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import json from '@rollup/plugin-json';

/**
 * 
 * @param {*} need 
 * @returns 
 */
const getCmmonPlugins = (need = false) => {
    return [
        ...(need ? [commonjs({
            include: [
                'axios', 'html2canvas', 'ua-parser-js', /form-data/, /follow-redirects/, /proxy-from-env/
            ]
        }),
        resolve()] : []),
        RollupTsPlugin(),
        json()
    ]
}


export default defineConfig([
    {
        input: 'lib/main.ts',
        output: {
            file: 'dist/esm/h-trackpoint.js',
            format: 'esm'
        },
        plugins: [...getCmmonPlugins()]
    },
    {
        input: 'lib/main.ts',
        output: {
            file: 'dist/cjs/h-trackpoint.js',
            format: 'cjs'
        },
        plugins: [...getCmmonPlugins(), copy({
            targets: [
                {
                    src: 'README.md',
                    dest: 'dist',
                    name: 'README.md'
                },
                {
                    src: 'types',
                    dest: 'dist',
                    name: 'types'
                }
            ]
        }), RollupGeneratePackageJSONPlugin({
            outputFolder: './dist',
            baseContents: {
                ...packageJSON,
                main: "cjs/h-trackpoint.js",
                module: "esm/h-trackpoint.js",
                unpkg: "umd/h-trackpoint.js",
            }
        })]
    },
])