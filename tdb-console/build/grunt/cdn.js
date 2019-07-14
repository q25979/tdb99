module.exports = {
    cdn: {
        "options": {
            "cdn": "<%= path.cdn %>",
            "flatten": true
        },
        "html": {
            "cwd": "<%= path.build%>/app/templates/",
            "dest": "<%= path.build%>/app/templates/",
            "src": "**/*.html"
        },
        "css": {
            "cwd": "<%= path.build%>/app/static/",
            "dest": "<%= path.build%>/app/static/",
            "src": ["assets/**/*.css", "components/**/*.css"]
        }
    }
};
