const path = require('path')

module.exports = {
    mode: 'development',
    entry: './src/index.js',
    output: {
        filename: 'bundle.js',
        path: path.join(__dirname, '../stoqu/static/js')
    },
    module: {
        rules: [
            {
                test: /\.js[x]?$/,
                exclude:/node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            '@babel/preset-env',
                            '@babel/preset-react'
                        ],
                        plugins: ['@babel/plugin-syntax-jsx']
                    }
                }
            }
        ]
    },
    resolve: {
        extensions: [
            '.js',
            '.jsx',
            '.json'
        ]
    }
};
