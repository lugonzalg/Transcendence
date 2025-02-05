const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack');

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack:{
    plugins:
    [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false',
      })
    ],
  },
}
),
{
  css: {
    loaderOptions: {
      sass: {
        implementation: require('sass'), // Para Sass
        // implementation: require('node-sass'), // Para SCSS
      },
    },
  },
}; 

