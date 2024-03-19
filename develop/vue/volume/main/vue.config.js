const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack');

<<<<<<< HEAD
module.exports = {
=======
module.exports = defineConfig({
  devServer: {
    allowedHosts: ['vue'],
  },
>>>>>>> 380f624b6a944076f389509f4e598fa2200f7e18
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false',
      }),
    ],
    module: {
      rules: [
        {
          test: /\.json$/,
          loader: 'json-loader',
          type: 'javascript/auto',
        },
      ],
    },
  },
  css: {
    loaderOptions: {
      sass: {
<<<<<<< HEAD
        implementation: require('sass'),
      },
    },
  },
};
=======
        implementation: require('sass')
      },
    },
  },
});
>>>>>>> 380f624b6a944076f389509f4e598fa2200f7e18
