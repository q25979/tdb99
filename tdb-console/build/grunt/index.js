/**
 * Created by huangdong on 5/25/16.
 */
const _ = require('lodash');

function buildConfigs(grunt, profile, callback) {
    var configs = {};

    function load(name) {
        var cfg = require('./' + name);
        if (typeof cfg.__init === 'function') {
            cfg.__init(grunt, profile);
            delete cfg.__init;
        }
        _.extend(configs, cfg);
    }

    [
        'abs',
        'clean',
        'copy',
        'imagemin',
        'cdn',
        'oss',
        'usemin',
        'filerev'
    ].map(load);
    return configs;
}

function loadTasks(grunt) {
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-compress');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-htmlmin');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-cdn');
    grunt.loadNpmTasks('grunt-filerev');
    grunt.loadNpmTasks('grunt-usemin');
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadTasks('grunt/tasks');
}

module.exports = function (grunt, callback) {
    var profile = require('./profile')(grunt);
    var configs = {
        configs: buildConfigs(grunt, profile),
        profile: profile
    };
    loadTasks(grunt);
    return configs;
};
