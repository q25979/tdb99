(function () {
    function createUploadEditor(editor, uploadUrl) {
        return $(editor).summernote({
            callbacks: {
                onImageUpload: function (files) {
                    var index = 0;

                    function next() {
                        if (index == files.length) {
                            return;
                        }
                        uploadImage(files[index++], uploadUrl, function (err, url) {
                            if (err) {
                                alert(err);
                            } else {
                                $(editor).summernote('editor.insertImage', url, function ($image) {
                                    $image.css('width', '100%');
                                });
                                next();
                            }
                        });
                    }

                    next();
                }
            }
        });
    }

    function uploadImage(file, url, callback) {
        var form_data = new FormData();
        form_data.append('image', file);
        $.ajax({
            data: form_data,
            type: 'POST',
            url: url,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                if (!data.success) {
                    return callback(data.message);
                }
                callback(null, data.url);
            },
            fail: function () {
                callback('fail');
            }
        })
    }

    window.createUploadEditor = createUploadEditor;
    window.uploadImage = uploadImage;
})();
