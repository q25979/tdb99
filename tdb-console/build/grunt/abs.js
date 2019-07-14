module.exports = {
    abs: {
        "options": {
            "root": "<%= path.build%>/app/",
            "flatten": true
        },
        "files": {
            "cwd": "<%= path.build%>/app/static",
            "dest": "<%= path.build%>/app/static/",
            "src": "**/*.css"
        }
    }
};
