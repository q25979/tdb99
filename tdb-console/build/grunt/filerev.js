module.exports = {
    filerev: {
        'options': {
            'algorithm': 'md5',
            'length': 3
        },
        'images': {
            'files': [{
                expand: true,
                cwd: '<%= path.build %>/app',
                src: ['static/**/*.{png,jpg,gif}'],
                dest: '<%= path.build %>/app/'
            }]
        },
        'css': {
            'src': [
                '<%= path.build %>/app/static/**/*.css',
                '!<%= path.build %>/app/static/js/skin/layer.css'
            ]
        },
        'js': {
            'src': [
                '<%= path.build %>/app/static/**/*.js'
            ]
        }
    }
};
