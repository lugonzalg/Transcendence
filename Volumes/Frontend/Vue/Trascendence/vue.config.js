const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
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

