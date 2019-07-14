var path = require('path');
var extend = require('extend');

module.exports = function (grunt) {
    var g = require('./grunt')(grunt);
    var gruntConfig = {
        path: g.profile.path,
        env: g.profile
    };
    extend(true, gruntConfig, g.configs);

    grunt.file.setBase(path.join(__dirname, '..'));
    grunt.initConfig(gruntConfig);
    grunt.registerTask(
        'build', [
            'clean:all',        //清楚数据
            'copy:build',       //拷贝数据
            'abs',              //处理绝对路径问题
            'imagemin',         //压缩图片
            'useminPrepare',
            // 'less',
            'concat',           //合并文件
            'uglify',           //压缩js 文件
            'cssmin',           //压缩css 文件
            'filerev:images',   //图片文件增加MD5
            'usemin:css',       //更新css 中图片的名称
            'cdn:css',          //css 中静态文件加 cdn 前缀
            'filerev:css',      //css 文件加 MD5
            'filerev:js',       //js  文件加 MD5
            'usemin:html',      //更新html 静态资源名称
            'cdn:html',         //html 中静态文件加 cdn 前缀
            'oss'               //上传oss
        ]
    );
};
