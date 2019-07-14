var path = require('path');

module.exports = function (grunt) {

    grunt.registerMultiTask('abs', 'make relative path absolute', function () {
        var root = this.options({root: '.'}).root;

        function compute(from, to) {
            var root = path.resolve(to);
            var sub = path.resolve(from);
            if (sub.indexOf(root) < 0) {
                return null;
            } else {
                return path.dirname(sub.substr(root.length));
            }
        }

        function absCSS(source, relativeRoot) {
            var rx = /url\s*\(["']?([^\)]+?)["']?\)/g;
            var m;
            var parts = [];
            var lastIndex = 0;
            while (m = rx.exec(source)) {
                parts.push(source.substring(lastIndex, m.index));
                var url = m[1];
                if (url.indexOf('data:') < 0 && url[0] != '/' && url.indexOf(':/') < 0) {
                    url = path.join(relativeRoot, url);
                }
                parts.push('url(');
                parts.push(url);
                parts.push(')');
                lastIndex = m.index + m[0].length;
            }
            if (parts.length == 0) {
                parts.push(source);
            } else if (lastIndex < source.length) {
                parts.push(source.substring(lastIndex));
            }
            return parts.join('');
        }

        //function absHTML(source, relativeRoot) {
        //    return source
        //        .replace(/(href=["'])\/(?!\/)/g, '$1' + relativeRoot)
        //        .replace(/(poster=["'])\/(?!\/)/g, '$1' + relativeRoot)
        //        .replace(/(src=["'])\/(?!\/)/g, '$1' + relativeRoot)
        //        .replace(/(assetpath=["'])\/(?!\/)/g, '$1' + relativeRoot)
        //        .replace(/(url=["'])\/(?!\/)/g, '$1' + relativeRoot)
        //        .replace(/(url\(['"]?)\/(?!\/)/g, "$1" + relativeRoot)
        //        .replace(/(content=["']0;url=)\/(?!\/)/g, "$1" + relativeRoot);
        //}

        function process(src, file) {
            var absFile = path.join(file.cwd, src);
            var relativeRoot = compute(absFile, root),
                extension = path.extname(src),
                filter, contents;
            if (!relativeRoot) {
                grunt.log.writeln('Failed to compute relative root for ' + src);
            }
            switch (extension) {
                case '.css':
                    filter = absCSS;
                    break;
                //case '.html':
                //    filter = absHTML;
                //    break;
                default:
                    grunt.warn('Unsupported extension ' + src);
                    return;
            }

            contents = grunt.file.read(absFile);
            contents = filter(contents, relativeRoot);
            grunt.file.write(path.join(file.dest, src), contents);
            grunt.log.writeln('Absolute ' + src);
        }

        this.files.forEach(function (file) {
            file.src.map(function (src) {
                process(src, file);
            });
        });
    });
};