'use strict';
var co = require('co');
var checksum = require('checksum');
var mime = require('mime-types')

module.exports = function (grunt) {

    var oss = require('ali-oss'),
        async = require('async'),
        path = require('path'),
        fs = require('fs'),
        chalk = require('chalk');

    grunt.registerMultiTask('oss', 'A grunt tool for uploading static file to aliyun oss.', function () {
        var done = this.async();
        // Merge task-specific and/or target-specific options with these defaults.
        var options = this.options({
            /**
             * @name objectGen --return a aliyun oss object name
             *                      default return grunt task files' dest + files' name
             * @param dest  --grunt task files' dest
             * @param src  --grunt task files' src
             */
            objectGen: function (dest, src) {
                return [dest, path.basename(src)].join('\/');
            }
        });
        if (!options.accessKeyId || !options.accessKeySecret || !options.bucket) {
            grunt.fail.fatal('accessKeyId, accessKeySecret and bucket are all required!');
        }
        var option = {
            accessKeyId: options.accessKeyId,
            accessKeySecret: options.accessKeySecret,
            bucket: options.bucket,
            region: options.region
        };
        var cache = {};
        if (grunt.file.exists(options.cache)) {
            cache = grunt.file.readJSON(options.cache);
        }
        var store = oss(option),
            uploadQue = [];
        // Iterate over all specified file groups.
        this.files.forEach(function (f) {
            // Concat specified files.
            var objects = f.src.filter(function (filepath) {
                // Warn on and remove invalid source files (if nonull was set).
                filepath = path.join(f.cwd, filepath);
                if (!grunt.file.exists(filepath)) {
                    grunt.log.warn('Source file "' + filepath + '" not found.');
                    return false;
                } else {
                    return true;
                }
            }).map(function (filepath) {
                // return an oss object.
                return {
                    bucket: options.bucket,
                    object: path.join(f.dest, filepath),
                    srcFile: path.join(f.cwd, filepath)
                };

            });
            objects.forEach(function (o) {
                uploadQue.push(o);
            });
        });
        var uploadTasks = [];
        uploadQue.forEach(function (o) {
            uploadTasks.push(makeUploadTask(o));
        });
        grunt.log.ok('Start uploading files.')
        async.series(uploadTasks, function (error, results) {
            if (options.cache) {
                grunt.file.write(options.cache, JSON.stringify(cache));
            }
            if (error) {
                grunt.fail.fatal("uploadError:" + JSON.stringify(error));
            } else {
                grunt.log.ok('All files has uploaded yet!');
            }
            done(error, results);
        });

        function buildOptions(obj) {
            var contentType = mime.lookup(obj.srcFile);
            var headers = {};
            if (options.headers) {
                for (var name in options.headers) {
                    if (options.headers.hasOwnProperty(name)) {
                        headers[name] = options.headers[name];
                    }
                }
            }
            if (contentType) {
                headers['Content-Type'] = contentType;
            }
            return {
                headers: headers
            };
        }

        /**
         * @name makeUploadTask  -- make task for async
         * @param object  --aliyun oss object
         */
        function makeUploadTask(o) {
            return function (callback) {
                //skip object when object's path is a directory;
                if (fs.lstatSync(o.srcFile).isDirectory()) {
                    callback();
                } else {
                    checksum.file(o.srcFile, function (err, sum) {
                        if (err) {
                            return callback(err);
                        }
                        if (cache[o.srcFile] == sum) {
                            callback();
                        } else {

                            grunt.log.ok('Uploading file ' + chalk.cyan(o.srcFile));
                            co(function * ()
                            {
                                "use strict";
                                var result = yield store.put(o.object, o.srcFile, buildOptions(o));
                                callback(null, result);
                                cache[o.srcFile] = sum;
                            }
                        ).
                            catch(function (err) {
                                callback(err, null);
                            });

                        }
                    });
                }
            }
        }
    });
};
