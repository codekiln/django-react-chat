/*********************************************************************
 * django react chat example project
 *
 * To start developing a webpack bundle, run `yarn watch` in your mac,
 *
 * This executes the script in the package.json at scripts['dev']:
 * `NODE_ENV=development webpack --config webpack.config.js --watch`
 *
 * Please see comments below explaining each element. If you change
 * anything, please update the comment.
 ********************************************************************/

  // webpack runs in node.js
  // this top section in nodejs is where modules use the `require()` call
  // to bring in any dependencies from node's core modules or `node_modules/` package path:

  // this is the node built-in path module: https://nodejs.org/api/path.html
const path = require('path');

// this is the webpack object, which is configured below.
// this comes from a dependency in package.json, which `yarn install` puts in ./node_modules/
const webpack = require('webpack');

// this is a tool we're using specifically to help django-webpack-loader
// add a templatetag that imports the correct bundle for a given file
// this comes from a dependency in package.json, which `yarn install` puts in ./node_modules/
const BundleTracker = require('webpack-bundle-tracker');


// In node, `module.exports` is how this
// js file declares what other node processes can run in this file.
// here, we're exporting webpack configuration information that
// webpack can make use of.
module.exports = [{

  // `context` here is like the basepath for resolving the entry points for bundles.
  // see `output` below for how that is configured.
  // https://webpack.js.org/configuration/entry-context/
  context: __dirname,
  entry: {

    // One entry here for every bundle for webpack to generate.
    // Format: 'bundle_identity_name': '/path/to/source/js/without/.js/suffix'
    'chat.rechat': './django_react_chat_example_project/static/js/chat/rechat/src/RechatMain',
    'chat.chat_app': './django_react_chat_example_project/static/js/chat/ChatApp/ChatApp',

  },

  // this section determines where bundles should be placed after they are generated.
  // https://webpack.js.org/concepts/output/
  output: {

    // all bundles will be put in this folder
    // go through normal collectstatic process, and that's where they will be minified
    // in time, we can get fancy, but this is a basic setup.
    path: path.resolve('./django_react_chat_example_project/static/js/webpack_bundles/'),

    // all bundles will have their same name from the `entry` section
    filename: '[name].js',
  },

  // https://webpack.js.org/configuration/devtool/
  // ensure that compiled assets have source map information inside, so that
  // the chrome debugger or other debuggers know how to display the source for
  // a given module
  devtool: 'eval-source-map',

  plugins: [
    // a webpack plugin is something that jacks into the webpack lifecycle
    // to do something useful. We're only using the django-centric
    // webpack-bundle-tracker, which is an npm/yarn package that outputs a mapping
    // of all the bundles to a json file. This is used by the `webpack_loader`
    // templatetag to insert the bundled file.
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  // in webpack, a "module" is something that can be referenced by
  // an import statement. Webpack constructs a dependency graph
  // from the import statements, and processes each module
  // using the rules below when constructing the webpack bundle.
  //
  // https://webpack.js.org/concepts/modules/
  module: {

    // this section defines the "rules" for importing modules
    // see https://webpack.js.org/concepts/modules/#supported-module-types
    // for a list of supported "loaders" aka transpilers.
    rules: [
      {
        // any files that end with `.js` will be processed with babel-loader
        // before creating the bundle.
        //
        // Babel makes it so you can use JS features that have become standard
        // but might not have made it into every single browser, (for example,
        // Object static methods or object destructuring),
        // and IF something isn't supported by the browser yet it will be shimmed.
        //
        // This picks up the configuration from the .babelrc file.
        test: /\.js$/,
        use: 'babel-loader',
        // ensure that we're not passing items from our node_modules folder to babel;
        // that stuff doesn't need to be processed
        exclude: /(node_modules)/
      },
      {
        // any files that end with .scss will be processed with
        // sass-loader first (sass to css), then css-loader, and finally style-laoder
        // before creating the bundle
        test: /\.scss$/,
        use: [
          {
            // https://yarnpkg.com/en/package/style-loader
            loader: 'style-loader' // creates style nodes from JS strings
          }, {
            // https://yarnpkg.com/en/package/css-loader
            loader: 'css-loader' // translates CSS into importable node modules so they can be bundled
          }, {
            // https://yarnpkg.com/en/package/sass-loader
            loader: 'sass-loader' // compiles Sass to CSS
          }
        ]
      },
      {
        test: /\.(graphql|gql)$/,
        exclude: /node_modules/,
        loader: 'graphql-tag/loader',
      },
    ]
  },

  // this section configures how `import 'path/to/mymodule'` resolves to
  // an actual file on the operating system
  // https://webpack.js.org/concepts/module-resolution/
  resolve: {

    // the 'modules' key here is a list of paths to search
    // inside for each importable element.
    // https://webpack.js.org/concepts/module-resolution/#module-paths
    modules: ['node_modules'],

    // if you put `import 'mylibrary/myfile.js', that will work just fine by default
    // by configuring the "extensions" that are automatically appended to the import
    // line, you can do `import 'mylibrary/myfile'` and it will resolve either
    // mylibrary/myfile.js or mylibrary/myfile.jsx
    // https://webpack.js.org/configuration/resolve/#resolve-extensions
    extensions: ['.js', '.jsx', '.json']
  },

}];
