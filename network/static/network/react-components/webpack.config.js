const path = require("path");

module.exports = {
    entry: {
        index: "./src/index.js",
        follow: "./src/follow.js",
    },
    output: {
        path: path.join(__dirname, "/bundles"),
        filename: "[name].bundle.js",
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                },
            },
        ],
    },
    resolve: {
        extensions: [".js", ".jsx"],
    },
};
