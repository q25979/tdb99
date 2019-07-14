var Utils = {};

/*
* 使用例子:  Utils.autocomplete('#inputId', '#codeId', 'www.baidu.com')
*/

Utils.autocomplete = function (inputId, codeId, url) {
    $(inputId).autocomplete({//保留 $("#inputId")
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
                url: url, //保留url: "exampleUrl",
                data: JSON.stringify(filterData),
                type: 'POST',
                json: true,
                contentType: 'application/json',
                success: function (data) {
                    var responseData = [];
                    for (var i = 0; i < data.data.length; i++) {
                        var item = data.data[i];
                        responseData.push({
                            'data': item.game_name,
                            'value': item.game_name,
                            'id': item.code
                        })
                    }
                    console.log(responseData);
                    done({suggestions: responseData});
                }

            });
        },
        onSelect: function (suggestion) {
            $(codeId).val(suggestion.id); //保留 $("#codeId").val(suggestion.id);
            console.log(suggestion.id);
        }
    });
}
