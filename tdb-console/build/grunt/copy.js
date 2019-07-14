module.exports = {
    copy: {
        build: {
            'files': [
                {
                    'expand': true,
                    'dest': '<%= path.build %>',
                    'src': [
                        'app/**',
                        'configuration/**',
                        'deploy/**',
                        'requirements/**',
                        'setup.py',
                        'supervisord.conf',
                        'run.py'
                    ]
                }
            ]
        }
    }
};
