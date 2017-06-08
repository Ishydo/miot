var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')
var ExtractTextPlugin = require('extract-text-webpack-plugin')

module.exports = {
  context: __dirname,
  entry: {
    main: './assets/main',
    frontend: './assets/frontend',
    dashboard: './assets/dashboard',
    dashboardmap: './assets/dashboard.map'
  },
  output: {
    path: path.resolve('./static/bundles/'),
    filename: "[name]-[hash].js",
  },
  plugins: [
    new webpack.ProvidePlugin({$: "jquery", jQuery: "jquery","window.jQuery": "jquery", "Tether": 'tether',}),
    new BundleTracker({filename: './webpack-stats.json'}),
    new ExtractTextPlugin('[name]-[contenthash].css')
  ],
  module: {
    loaders: [
      // Expose jquery! Necessary for templates media such as {{form.media}}
      { test: require.resolve('jquery'), loader: 'expose-loader?jQuery!expose-loader?$' },
      { test: require.resolve('sortablejs'), loader: 'expose-loader?Sortable'},
      { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "url-loader?limit=10000&mimetype=application/font-woff" },
      { test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: "file-loader" },
      { test: /\.(jpe?g|png|gif)$/i,
        loaders: [
            'file-loader?hash=sha512&digest=hex&name=[hash].[ext]',
            'image-webpack-loader?bypassOnDebug&optimizationLevel=7&interlaced=false'
        ]
      },
      { test: /\.jsx?$/,
      use: [
        {
          loader: 'babel-loader',
          options: {
            presets: [
              ['latest']
            ]
          }
        }
      ]
    },
      {
        test: /\.s?css$/,
        use: ExtractTextPlugin.extract({
          fallback: "style-loader",
          loader: ['css-loader', 'sass-loader']
        })
      },
      {
      test: require.resolve('tinymce/tinymce'),
      loaders: [
        'imports-loader?this=>window',
        'exports-loader?window.tinymce'
      ]
    },
    {
      test: /tinymce\/(themes|plugins)\//,
      loaders: [
        'imports-loader?this=>window'
      ]
    }
    ],
  },
}
