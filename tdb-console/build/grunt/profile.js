module.exports = function (grunt) {
    var target = grunt.option('target') || 'staging';
    var production = target == 'production';
    var appName = '';
    var profiles = {
        production: {
            oss: {
                accessKeyId: 'LTAId5JGkZzEFYSw',
                accessKeySecret: 'y9DCNzafnatLMxE1s7IxqvI5NlQe0M',
                bucket: 'xiaoyu168',
                region: 'oss-ap-southeast-1',
                prefix: appName + '/'
            },
            path: {
                build: 'build/temp',
                dist: 'build/dist',
                cdn: '/' + appName
            }
        },
        staging: {
            oss: {
                accessKeyId: 'LTAId5JGkZzEFYSw',
                accessKeySecret: 'y9DCNzafnatLMxE1s7IxqvI5NlQe0M',
                bucket: 'xiaoyu168',
                region: 'oss-ap-southeast-1',
                prefix: appName + '/'
            },
            path: {
                build: 'build/temp',
                staging: 'build/staging',
                dist: 'build/dist',
                cdn: '/' + appName
            }
        }
    };

    return profiles[target];
};
