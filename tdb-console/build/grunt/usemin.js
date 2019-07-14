const path = require('path');

var lessCreateConfig = function (context, block) {
    var cfg = {files: []},
        filesDef = {};

    filesDef.dest = path.join(context.outDir, block.dest);
    filesDef.src = [];

    context.inFiles.forEach(function (inFile) {
        filesDef.src.push(path.join(context.inDir, inFile));
    });

    cfg.files.push(filesDef);
    context.outFiles = [block.dest];
    return cfg;
};

var lessBlockReplacement = function (block) {
    return '<link rel="stylesheet" href="' + block.dest + '" />';
};


module.exports = {
    useminPrepare: {
        'templates': {
            'options': {
                'dest': '<%= path.build %>/app',
                'root': '<%= path.build %>/app',
                'type': 'html'
            },
            'files': {
                'src': '<%= path.build %>/app/templates/**/*.html'
            }
        },
        options: {
            flow: {
                steps: {
                    'less': [{
                        name: 'less',
                        createConfig: lessCreateConfig
                    }, 'cssmin'],
                    'css': ['concat', 'cssmin'],
                    'js': ['concat', 'uglify']
                }
            },
            staging: '<%= path.staging %>'
        }
    },
    usemin: {
        'html': [
            '<%= path.build %>/app/templates/**/*.html'
        ],
        'css': [
            '<%= path.build %>/app/static/**/*.css'
        ],
        'options': {
            assetsDirs: [
                '<%= path.build %>',
                '<%= path.build %>/app'
            ],
            blockReplacements: {
                less: lessBlockReplacement
            }
        }
    }
};
