module.exports = {
    oss: {
        upload: {
            options: {
                accessKeyId: '<%= env.oss.accessKeyId %>',
                accessKeySecret: '<%= env.oss.accessKeySecret %>',
                bucket: '<%= env.oss.bucket %>',
                region: '<%= env.oss.region %>',
                cache: '<%= path.build %>/../oss-cache.json',
                headers: {
                    'Cache-Control': 'max-age=86400, public',
                    'Access-Control-Allow-Origin': '*'
                }
            },
            files: [{
                'cwd': '<%= path.build %>/app/static',
                'src': '**',
                'dest': '<%= env.oss.prefix %>static'
            }]
        }
    }
};