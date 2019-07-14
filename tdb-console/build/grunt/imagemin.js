module.exports = {
    imagemin: {
        static: {
            files: [{
                expand: true,
                cwd: '<%= path.build %>/app',
                src: ['static/**/*.{png,jpg,gif}'],
                dest: '<%= path.build %>/app/'
            }]
        }
    }
};