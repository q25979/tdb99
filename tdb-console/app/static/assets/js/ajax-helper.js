(function ($) {

    // 处理 401 错误, 重定向到登录页
    $(document).ajaxComplete(function (event, xhr, settings) {
        if (xhr.status == 401) {
            layer.msg('登录失效, 请重新登录');
            setTimeout(function () {
                window.location = xhr.responseJSON.redirect;
            }, 3000);
        } else if (xhr.status == 500) {
            layer.alert('系统错误');
        }
    });

    // 清除错误信息
    $.fn.resetFieldErrors = function (additionalFields) {
        var $form = $(this);

        function reset(element) {
            var group = $(element).closest('.form-group');
            group.removeClass('has-error');
            // $(element).popover('hide');
        }

        $form.find('input').each(function () {
            reset(this);
        });
        if (Array.isArray(additionalFields)) {
            for (var i = 0; i < additionalFields.length; i++) {
                reset(additionalFields[i]);
            }
        }
        return this;
    };

    // ajax 提交表单
    $.fn.ajaxSubmit = function (data, callback) {
        if (typeof data === 'function') {
            callback = data;
            data = $(this).serialize();
        }
        var url = $(this).attr('action');
        return $.post(url, data, callback);
    };

    // 将服务端的数据验证信息显示到 form 里面对应的域中
    $.fn.applyFieldErrors = function (errors, options) {
        var $form = $(this);
        if (!options) {
            options = {};
        }
        if (typeof errors['statusCode'] === 'function') {
            if (errors.status != 400 || (errors.responseJSON.code != 400 && errors.responseJSON.code != 1000)) {
                return false;
            }
            errors = errors.responseJSON.message;
        }
        var defaultErrorHandlers = {
            'popover': function (target, error) {
                $(target).popover({
                    content: error,
                    placement: 'bottom',
                    trigger: 'hover'
                }).popover('show');
            },
            'highlight': function (target, error) {
                var group = $(target).closest('.form-group');
                group.addClass('has-error');
            },
            'error-label': function (target, error) {
                var group = $(target).closest('.form-group');
                defaultErrorHandlers.highlight(target, error);
                group.find('.error-label').text(error);
            },
            'popover-and-highlight': function (target, error) {
                defaultErrorHandlers.highlight(target, error);
                defaultErrorHandlers.popover(target, error);
            }
        };

        var errorHandler = options.handler;
        if (typeof errorHandler === 'string') {
            errorHandler = defaultErrorHandlers[errorHandler];
        }

        if (!errorHandler) {
            errorHandler = defaultErrorHandlers['popover'];
        }

        function findTarget(name) {
            if (typeof options.mapping === 'function') {
                return $(options.mapping(name));
            } else if (typeof options.mapping === 'object' && options.mapping[name]) {
                return $(options.mapping[name]);
            }
            var target = $form.find('#' + name);
            if (!target) {
                target = $form.find('name=[' + name + ']');
            }
            return target;
        }

        function showError(name, index, error) {
            var target = findTarget(name);
            if (target && errorHandler) {
                errorHandler(target, error);
            }
        }

        for (var field in errors) {
            if (!errors.hasOwnProperty(field)) {
                continue;
            }
            var messages = errors[field];
            if (typeof(messages) === 'string') {
                showError(field, null, messages);
            } else {
                for (var prop in messages) {
                    if (messages.hasOwnProperty(prop)) {
                        showError(field, prop, messages[prop]);
                    }
                }
            }
        }
        return errors;
    };

    (function () {
        function dataTableLoader(url, filterForm) {
            return function (data, callback, settings) {
                var query = {};
                if (filterForm) {
                    var filters = $(filterForm).serializeObject();
                    $.each(filters, function (k, v) {
                        if (v) {
                            query[k] = v;
                        }
                    });
                }
                data.length = data.length || 50;
                query.per_page = data.length;
                query.page = data.start / data.length + 1;
                data.query = query;
                $.ajax({
                    url: url,
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: callback
                }).error(function () {
                    layer.msg('数据加载失败');
                    callback({error: '加载失败', data: [], draw: data.draw, recordsTotal: 0, recordsFiltered: 0});
                });
            }
        }

        function formatDatetime(date, format) {
            var unixTimestamp = new Date(date * 1000);  // convert to unix timestamp
            date = new Date(unixTimestamp); //新建日期对象

            /* 日期字典 */
            var map = {
                "M": date.getMonth() + 1, //月份
                "d": date.getDate(), //日
                "h": date.getHours(), //小时
                "m": date.getMinutes(), //分
                "s": date.getSeconds(), //秒
                "q": Math.floor((date.getMonth() + 3) / 3), //季度
                "S": date.getMilliseconds() //毫秒
            };

            /* 正则替换 */
            format = format.replace(/([yMdhmsqS])+/g, function (all, t) {
                var v = map[t];
                if (v !== undefined) {
                    if (all.length > 1) {
                        v = '0' + v;
                        v = v.substr(v.length - 2);
                    }
                    return v;
                }
                else if (t === 'y') {
                    return (date.getFullYear() + '').substr(4 - all.length);
                }
                return all;
            });

            /* 返回自身 */
            return format;
        }

        window.formatDatetime = formatDatetime;

        function dataTableConfig(options) {
            var defaults = {
                'sPaginationType': 'full_numbers',//显示数字的翻页样式
                'bLengthChange': false,
                'searching': false,
                'pageLength': 50,
                'processing': true,
                'ordering': true,
                'oLanguage': {
                    'sZeroRecords': '抱歉， 没有找到',
                    'sInfo': '从 _START_ 到 _END_ /共 _TOTAL_ 条数据',
                    'sInfoEmpty': '没有数据',
                    'sInfoFiltered': '(从 _MAX_ 条数据中检索)',
                    'oPaginate': {
                        'sFirst': '首页',
                        'sPrevious': '前一页',
                        'sNext': '后一页',
                        'sLast': '尾页'
                    },
                }
            };
            return $.extend(defaults, options);
        }

        var dataRenders = {
            date: function () {
                return function (data, type, row) {
                    if (data) {
                        return formatDatetime(parseInt(data), 'yyyy-MM-dd hh:mm:ss');
                    }
                    else {
                        return '-';
                    }
                }
            },
            tmpl: function (template) {
                return function (data, type, row, meta) {
                    return $('<div>').append($(template).tmpl({data: data, row: row, type: type, meta: meta})).html();
                }
            },
            dict: function (dict) {
                return function (data, type, row) {
                    return dict[data];
                }
            },
            image: function (className) {
                return function (data, type, row) {
                    return $('<div>').append($('<img>').addClass(className).attr('src', data)).html();
                }
            },
            rowSelector: function (dynamic) {
                return function (data, type, row) {
                    if (dynamic) {
                        return '<span class="row-select-checkbox"></span>';
                    }
                    else if (data) {
                        return '<span class="row-select-checkbox"></span>';
                    }
                    else
                        return ''

                };
            },
            flagCheck: function (value) {
                return function (data, type, row) {
                    var widget = $('<div class="icon-change"><i class="fa fa-check"></i><i class="fa fa-times none"></i></div>');
                    if ((parseInt(data) & value) != value) {
                        widget.addClass('icon-remove text-danger');
                    }
                    else {
                        widget.addClass('icon-ok text-success');
                    }
                    return $('<div>').append(widget).html();
                }
            },
            fixed: function (value) {
                return function () {
                    return value;
                }
            },
            text: function () {
                return function (data) {
                    if (!data) {
                        data = '-'
                    }
                    return $('<div>').text(data).html();
                };
            },
            currency: function () {
                return function (data) {
                    return $('<div>').text(parseFloat(data).toFixed(4)).html();
                }
            },
            float: function () {
                return function (data) {
                    return $('<div>').text(parseFloat(data)).html();
                }
            }
        };
        window.dtUtils = {
            dataLoader: dataTableLoader,
            config: dataTableConfig,
            renders: dataRenders,
            columns: {
                rowSelector: function (dynamic, prop, options) {
                    var def = {
                        orderable: false,
                        className: 'select-checkbox',
                        targets: 0,
                        data: prop
                    };

                    def.render = dataRenders.rowSelector(dynamic);

                    return $.extend(def, options);
                },
                fixed: function (value, options) {
                    return $.extend({
                        orderable: false,
                        render: dataRenders.fixed(value)
                    }, options);
                },
                flag: function (value, prop, options) {
                    return $.extend({
                        orderable: false,
                        data: prop,
                        render: dataRenders.flagCheck(value)
                    }, options);
                },
                tmpl: function (prop, template, options) {
                    return $.extend({
                        orderable: false,
                        data: prop,
                        render: dataRenders.tmpl(template)
                    }, options);
                },
                text: function (prop, options) {
                    return $.extend({
                        orderable: false,
                        data: prop,
                        render: dataRenders.text()
                    }, options);
                },
                date: function (prop, options) {
                    return $.extend({
                        orderable: false,
                        data: prop,
                        render: dataRenders.date()
                    }, options);
                },
                image: function (prop, imageClassName, options) {
                    return $.extend({
                        orderable: false,
                        data: prop,
                        render: dataRenders.image(imageClassName)
                    }, options);
                },
                currency: function (prop, options) {
                    return $.extend({
                        orderable: false,
                        data: prop,
                        render: dataRenders.currency()
                    }, options);
                },
                dict: function (prop, dict, options) {
                    return $.extend({
                        orderable: false,
                        data: prop,
                        render: dataRenders.dict(dict)
                    }, options);
                },
                float: function (prop, options) {
                    return $.extend({
                        orderable: false,
                        data: prop,
                        render: dataRenders.float()
                    }, options);
                }
            },
            bindSelectCheckbox: function (table) {
                $(table.header()).on('click', '.row-select-checkbox', function () {
                    if ($(this).closest('tr').hasClass('selected')) {
                        table.rows().deselect();
                    } else {
                        table.rows().select();
                    }
                });
                table.on('select', function (e, dt, type, indexes) {
                    if (table.rows('.selected')[0].length == table.rows()[0].length) {
                        $(table.header()).children('tr').addClass('selected');
                    }
                }).on('deselect', function (e, dt, type, indexes) {
                    $(table.header()).children('tr').removeClass('selected');
                });
            }
        };
    })();

    $(document).on('processing.dt', '.data-table', function (e, settings, processing) {
        var $spinner = $(this).siblings('.dataTables_processing');
        if (processing) {
            $spinner.html('<div class="sk-fading-circle">' +
                '<div class="sk-circle1 sk-circle"></div>' +
                '<div class="sk-circle2 sk-circle"></div>' +
                '<div class="sk-circle3 sk-circle"></div>' +
                '<div class="sk-circle4 sk-circle"></div>' +
                '<div class="sk-circle5 sk-circle"></div>' +
                '<div class="sk-circle6 sk-circle"></div>' +
                '<div class="sk-circle7 sk-circle"></div>' +
                '<div class="sk-circle8 sk-circle"></div>' +
                '<div class="sk-circle9 sk-circle"></div>' +
                '<div class="sk-circle10 sk-circle"></div>' +
                '<div class="sk-circle11 sk-circle"></div>' +
                '<div class="sk-circle12 sk-circle"></div>' +
                '</div>')
        }
    });
})($);
