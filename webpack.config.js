const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
    entry: '/src/index.js',
    output: {
      path: __dirname + '/dist',
      filename: 'index_bundle.js'
    },
    plugins: [
      new HtmlWebpackPlugin({
        filename: 'index.html',
        template: '/public/index.html'
      })
    ]
  }