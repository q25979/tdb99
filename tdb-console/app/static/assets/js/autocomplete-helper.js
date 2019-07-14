/**
 * Created by zhuangqiuyu on 2017/5/18.
 */
(function ($) {
    $.fn.autoComplete = function (option) {

        $(this).autocomplete({
            minChars: 0,
            lookup: function (query, done) {
                var filterData = {
                    draw: 1,
                    query: {
                        status: 7,
                        game_name: query,
                        per_page: 5
                    }
                };
                $.ajax({
                    url: option.url,
                    data: JSON.stringify(filterData),
                    type: 'POST',
                    json: true,
                    contentType: 'application/json',
                    success: function (data) {
                        var responseData = [];
                        for (var i = 0; i < data.data.length; i++) {
                            var item = data.data[i];
                            responseData.push({
                                'data': item[option.name],
                                'value': item[option.name],
                                'id': item[option.value]
                            })
                        }
                        $(option.field).val('');
                        done({suggestions: responseData});
                    }

                });
            },
            onSelect: function (suggestion) {
                $(option.field).val(suggestion.id);
            }
        });
    }

})($);

// $("#game_name_search").autoComplete({
//     url: "{{ url_for('game.ajax_list') }}",
//     name: 'game_name',
//     value: 'code',
//     field: '#game_code'
// });