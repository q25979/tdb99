function binaryTree(type, opts) {
    var $tree = $(opts.id), $wrap = $tree.find('.wrap'), $struct = $tree.find('.struct');
    var temp = {
        refresh: '<div class="refresh"></div>',
        branch: {
            3: '<div class="branch"><div class="line line-10"></div><div class="two"><div></div></div></div>',
            2: '<div class="branch"><div class="line line-10"></div><div class="two"></div></div>',
            1: '<div class="line line-20"></div>',
            0: ''
        },
        line20: '<div class="line line-20"></div>',
        cb: '<div class="cb"></div>'
    };

    ajax(opts.unique_id);

    //刷新
    $struct.on('click', '.refresh', function () {
        ajax(opts.unique_id);
    });

    //上钻
    $struct.on('click', '.parent', function () {
        ajax($(this).attr('data-parent'));
    });

    //下钻
    $struct.on('click', '.user dt.clicked', function () {
        $(this).append('<div class="loading"></div>');
        ajax($(this).closest('.user').find('.number').text());
    });

    //search
    opts.searchBtn.on('click', function() {
        ajax(opts.searchInput.val());
    });

    //tip
    $struct.on({
        mouseenter: function () {
            var $tip = $(this).find('dd').show(), treeTop = $tree.offset().top;
            var w = Math.min($(window).width(), $('body').outerWidth(true), $tree.outerWidth(true));
            var offset = $(this).offset(), tipW = $tip.outerWidth(true), tipH = $tip.outerHeight(true),
                fixW = $(this).width(), fixH = $(this).height();
            if (w - offset.left - fixW >= tipW) {//right
                $tip.css('left', '100%');
            } else {//right
                $tip.css('left', '-' + tipW + 'px');
            }
            if (offset.top - treeTop < tipH) {//bottom
                $tip.css('top', 0);
            } else {//top
                if (treeTop + $tree.outerHeight() - offset.top >= tipH) {
                    $tip.css('top', 0);
                } else {
                    $tip.css('bottom', 0);
                }
            }
        },
        mouseleave: function () {
            $(this).find('dd').removeAttr('style').hide();
        }
    }, '.user>dl');

    function initPlacementData(data, depth) {
        return {
            "info": {
                "number": data.uid,
                "level": "1",
                "icon": 1
            },
            uid: data.uid,
            parent: data.placement_uid,
            nickname: data.nickname,
            sponsored_count: data.sponsored_count,
            team_a_investment: data.team_a_investment,
            team_b_investment: data.team_b_investment,
            created_at: getTime(data.created_timestamp),
            depth: depth + 1
        };

    };

    function getTime(time) {
        var date = new Date(time * 1000);
        date.getFullYear();
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDate();
        var hours = date.getHours();
        var minutes = date.getMinutes();
        var seconds = date.getSeconds();
        // return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds;
        return year + '-' + month + '-' + day;
    }

    function ajax(number) {
        $.ajax({
            type: 'POST',
            url: opts.url,
            dataType: 'json',
            data: JSON.stringify({depth: 4, unique_id: number}),
            contentType: 'application/json',
            success: function (data) {
                var treeData = {};
                var flag = 1;
                var objects = data.objects;

                function getData(treeData) {
                    var child = [];
                    if (flag === 1) {
                        treeData.info = {
                            "number": objects[0].uid,
                            "level": "1",
                            "icon": 1
                        };
                        treeData.uid = objects[0].uid;
                        treeData.nickname = objects[0].nickname;
                        treeData.created_at = getTime(objects[0].created_timestamp);
                        treeData.sponsored_count = objects[0].sponsored_count;
                        treeData.team_a_investment = objects[0].team_a_investment;
                        treeData.team_b_investment = objects[0].team_b_investment;
                        treeData.depth = 1;
                        flag += 1;
                        if (number != opts.unique_id) {
                            treeData.parent = objects[0].placement_uid;
                        }
                    }
                    objects.forEach(function (item) {
                        if (item.placement_uid == treeData.uid) {
                            child.push(item);
                        }
                    });
                    if (child.length) {
                        child.forEach(function (item) {
                            if (item.position === 0) {
                                if (treeData.depth < 3) {
                                    treeData.left = initPlacementData(item, treeData.depth);
                                    getData(treeData.left);
                                }
                                else {
                                    treeData.position = {
                                        left: false,
                                        right: false

                                    }
                                }
                            }
                            if (item.position === 1) {
                                if (treeData.depth < 3) {
                                    treeData.right = initPlacementData(item, treeData.depth);
                                    getData(treeData.right);
                                }
                                else {
                                    treeData.position = {
                                        left: false,
                                        right: false
                                    }
                                }

                            }
                        })
                    } else {
                        if (treeData.depth < 3) {
                            treeData.position = {
                                left: true,
                                right: true
                            }
                        } else {
                            treeData.position = {
                                left: false,
                                right: false
                            }
                        }
                    }
                    if (child.length === 1 && treeData.depth < 3) {
                        if (child[0].position === 0) {
                            treeData.position = {
                                right: true
                            }
                        } else {
                            treeData.position = {
                                left: true
                            }
                        }
                    }
                }

                if (objects.length) {
                    getData(treeData);
                }
                update(number, treeData);
            },
            error: function (err) {
                layer.msg('无此编号');
            }
        });
    }

    function update(number, data) {
        var html = '';
        if (opts.unique_id == number) {
            html += temp.refresh;
        } else {
            html += '<div class="parent" data-parent="' + data.parent + '"></div>';
        }
        var sW;
        html += renderBlock(data);
        $tree.css('overflow', 'hidden');
        $wrap.width(100000);
        $struct.html(html).css('opacity', 0);
        sW = $struct.width();
        $wrap.width(sW);
        $tree.css('overflow', 'auto');
        $struct.find('.branch').each(function (i, b) {
            var $b = $(b), $nextLeft = $b.nextAll('.left').eq(0), mL = 0, mR = 0;
            var $nextLeftLine = $nextLeft.find('.line').eq(0);
            var $nextLeftLineParent = $nextLeftLine.parent().parent();
            mL = $nextLeftLine.offset().left - $nextLeftLineParent.offset().left;
            $b.css('margin-left', mL);
            var $nextRight = $b.nextAll('.block').eq(-1);
            var $nextRightLine = $nextRight.find('.line').eq(0);
            var $nextRightLineParent = $nextRightLine.parent().parent();
            mR = $nextRightLine.offset().left - $nextRightLineParent.offset().left;
            $b.css('margin-right', mR);
            var $bLine = $b.find('.line');
            var $userLine = $b.prevAll('.user').eq(0).find('.line');
            mL = $userLine.offset().left - $b.offset().left;
            $bLine.css('margin-left', mL);
            var $bMidLine = $b.find('.two>div');
            if ($bMidLine.length) {
                var $midLine = $b.nextAll('.middle').eq(0).find('.line').eq(0);
                $bMidLine.css('margin-left', $midLine.offset().left - $nextLeftLine.offset().left - 2);
            }
        });
        $struct.hide().css('opacity', 1).fadeIn();
    }

    function renderUser(data) {
        return '<div class="user"><dl><dt class="icon_' + data.info.icon + ' clicked">' +
            // '<span class="'+data.status+'"></span>' +
            '</dt><dd>' + opts.toolTip(data) + '</dd></dl><div class="line line-10"></div><div class="number color_' + data.info.level + '" status=' + data.status + '>' + data.info.number + '</div></div>';
    }

    function renderAdd(parent, pos) {
        return '<div class="user"><dl><dt class="icon_7">' +
            // '<span class="'+data.status+'"></span>' +
            '</dt></dl><div class="line line-10"></div><div class="number text green">无用户</div></div>';
    }

    function renderBlock(data) {
        var user = renderUser(data), html = '', callee = arguments.callee, branch = {};
        data = $.extend({position: {}}, data);
        if (data.left) {
            html += '<div class="left block">' + callee(data.left) + '</div>';
            branch.left = true;
        } else if (data.position.left) {
            html += '<div class="left block">' + renderAdd(data.id, 'left') + '</div>';
            branch.left = true;
        }
        if (3 == type) {
            if (data.middle) {
                html += '<div class="middle block">' + callee(data.middle) + '</div>';
                branch.middle = true;
            } else if (data.position.middle) {
                html += '<div class="middle block">' + renderAdd(data.id, 'middle') + '</div>';
                branch.middle = true;
            }
        }
        if (2 == type || 3 == type) {
            if (data.right) {
                html += '<div class="right block">' + callee(data.right) + '</div>';
                branch.right = true;
            } else if (data.position.right) {
                html += '<div class="right block">' + renderAdd(data.id, 'right') + '</div>';
                branch.right = true;
            }
        }

        var cnt = 0;
        for (var i in branch) {
            cnt++;
        }
        return user + temp.branch[cnt] + html;
    }
}