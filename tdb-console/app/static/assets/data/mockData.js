var mockData = function (number) {
    var tip={
        "name": "张三",
        "level": "一级",
        "left-amount": "左区业绩",
        "right-amount": "右区业绩",
        "total-amount":"总业绩",
        "time": "2016-7-6 10:21:19"
    };
    var data=(function(){
        var left_1_1={
            "info": {
                "number": "left-1-1",
                "level": "1",
                "icon": 3
            },
            "tip":tip,
            status:'active',
            parent:'left-1'
        };
        var left_2_1={
            "info": {
                "number": "left-2-1",
                "level": "6",
                "icon": 3
            },
            "tip":tip,
            status:'locked',
            parent:'left-2'
        };
        var left_1={
            "info": {
                "number": "left-1",
                "level": "1",
                "icon": 2
            },
            "tip":tip,
            left:left_1_1,
            position:{
                middle:true,
                right:true
            },
            status:'inactive',
            parent:'left'
        };
        var left_2={
            "info": {
                "number": "left-2",
                "level": "1",
                "icon": 4
            },
            "tip":tip,
            left:left_2_1,
            status:'locked',
            parent:'left'
        };
        var left_3_1={
            "info": {
                "number": "left-3-1",
                "level": "1",
                "icon": 3
            },
            "tip":tip,
            status:'active',
            parent:'left-3'
        };
        var left_3={
            "info": {
                "number": "left-3",
                "level": "1",
                "icon": 4
            },
            "tip":tip,
            left:left_3_1,
            position:{
                right:true
            },
            status:'inactive',
            parent:'left'
        };

        var left={
            "info": {
                "number": "left",
                "level": "1",
                "icon": "1"
            },
            "tip":tip,
            left:left_1,
            middle:left_2,
            right:left_3,
            status:'locked',
            parent:'root'
        };

        var mid_1_1={
            "info": {
                "number": "mid-1-1",
                "level": "1",
                "icon": 3
            },
            "tip":tip,
            status:'active',
            parent:'mid-1'
        };
        var mid_1_2={
            "info": {
                "number": "mid-1-2",
                "level": "1",
                "icon": 3
            },
            "tip":tip,
            status:'inactive',
            parent:'mid-1'
        };

        var mid_1={
            "info": {
                "number": "mid-1",
                "level": "1",
                "icon": 2
            },
            "tip":tip,
            left:mid_1_1,
            middle:mid_1_2,
            status:'locked',
            parent:'middle'
        };
        var mid_2_1={
            "info": {
                "number": "mid-2-1",
                "level": "1",
                "icon": 3
            },
            "tip":tip,
            status:'active',
            parent:'mid-2'
        };
        var mid_2_3={
            "info": {
                "number": "mid-2-3",
                "level": "1",
                "icon": 3
            },
            "tip":tip,
            status:'inactive',
            parent:'mid-2'
        };

        var mid_2={
            "info": {
                "number": "mid-2",
                "level": "1",
                "icon": 4
            },
            "tip":tip,
            left:mid_2_1,
            right:mid_2_3,
            "position": {
                middle:true
            },
            status:'locked',
            parent:'middle'
        };
        var mid_3_1={
            "info": {
                "number": "mid-3-1",
                "level": "1",
                "icon": 2
            },
            "tip":tip,
            status:'active',
            parent:'mid-3'
        };
        var mid_3={
            "info": {
                "number": "mid-3",
                "level": "1",
                "icon": 4
            },
            "tip":tip,
            right:mid_3_1,
            "position": {
                left:true
            },
            status:'inactive',
            parent:'middle'
        };

        var mid={
            "info": {
                "number": "mid",
                "level": "6",
                "icon": "1"
            },
            "tip":tip,
            left:mid_1,
            middle:mid_2,
            right:mid_3,
            status:'locked',
            parent:'root'
        };

        var right_1_1={
            "info": {
                "number": "right-1-1",
                "level": "1",
                "icon": 2
            },
            "tip":tip,
            status:'active',
            parent:'right-1'
        };
        var right_1={
            "info": {
                "number": "right-1",
                "level": "1",
                "icon": 1
            },
            "tip":tip,
            position:{
                right:1
            },
            status:'inactive',
            parent:'right'
        };
        var right_2={
            "info": {
                "number": "right-2",
                "level": "1",
                "icon": "1"
            },
            "tip":tip,
            "position": {
                left:true,
                middle:true,
                right:true
            },
            status:'locked',
            parent:'right'
        };
        var right_3={
            "info": {
                "number": "right-3",
                "level": "1",
                "icon": "1"
            },
            "tip":tip,
            "position": {
                left:true,
                middle:true,
                right:true
            },
            status:'active',
            parent:'right'
        };
        var right={
            "info": {
                "number": "right",
                "level": "1",
                "icon": 5
            },
            "tip":tip,
            "left": right_1,
            "middle": right_2,
            "right": right_3,
            status:'inactive',
            parent:'root'
        };

        return {
            root:{
                "info": {
                    "number": "root",
                    "level": "1",
                    "icon": 1
                },
                "tip":tip,
                left:left,
                middle:mid,
                right:right,
                status:'active'
            },

            left:left,
            'left-1-1':left_1_1,
            'left-1':left_1,
            'left-2':left_2,
            'left-2-1':left_2_1,
            'left-3':left_3,
            'left-3-1':left_3_1,

            middle:mid,
            'mid-1':mid_1,
            'mid-2':mid_2,
            'mid-2-1':mid_2_1,
            'mid-2-3':mid_2_3,
            'mid-3':mid_3,
            'mid-3-1':mid_3_1,
            'mid-1-1':mid_1_1,
            'mid-1-2':mid_1_2,

            right:right,
            'right-1':right_1,
            'right-2':right_2,
            'right-3':right_3,
            'right-1-1':right_1_1
        }
    })();
    return data[number]?data[number]:{error:{code:404,message:'Not Found'}};
};