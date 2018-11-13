String.format = function() {
    var s = arguments[0];
    for (var i = 0; i < arguments.length - 1; i++) {
        var reg = new RegExp("\\{" + i + "\\}", "gm");
        s = s.replace(reg, arguments[i + 1]);
    }

    return s;
};

//loading animation
var $loading = $('#loading').hide();
$(document)
    .ajaxStart(function () {
        $loading.show();
    })
    .ajaxStop(function () {
        $loading.hide();
    });

//form related
var default_input_csv_string = 'Veh_No,SOB,MC101,MC201,MC301,RF101,RF201,RF301,FF101,UB101,BS101,CL100,CL101,CL102,BS201,FI101,FO101,LS101,A metric,B metric,CL201,AS101,BS Audit,C metric\n' +
    '1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '2,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0\n' +
    '3,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '4,10,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0\n' +
    '5,11,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1\n' +
    '6,12,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '7,13,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '8,14,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '9,15,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '10,16,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '11,17,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '12,18,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1\n' +
    '13,19,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '14,20,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '15,21,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1\n' +
    '16,22,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '17,23,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1\n' +
    '18,24,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '19,25,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0\n' +
    '20,26,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '21,27,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '22,28,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0\n' +
    '23,29,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1\n' +
    '24,30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0\n' +
    '25,31,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0';

var input_json = Papa.parse(default_input_csv_string);
console.log(input_json);

var veh_list = $('#form_container #veh_list');
var veh_item_template = '<tr data-id="{0}">\n' +
    '            <th scope="row">xxx-xxx-xx{1}</th>\n' +
    '            <td>{2}</td>\n' +
    '            <td>{3}</td>\n' +
    '            <td>\n' +
    '                <button type="button" class="btn btn-link btn-sm edit">Edit</button>\n' +
    '                <button type="button" class="btn btn-link btn-sm delete">Delete</button>\n' +
    '            </td>\n' +
    '        </tr>';

render_veh_list(input_json);
function render_veh_list(json) {
    for(var i = 1; i < json.data.length; i++) {
        veh_list.append(String.format(veh_item_template, json.data[i][0], json.data[i][0], json.data[i][1], json.data[i].join('-')));
    }
    bind_edit_del_events();
}

function bind_edit_del_events() {
    $('#form_container #veh_list .edit').click(function () {
        console.log('edit');
        console.log(get_click_item_index($(this)));
    });
    $('#form_container #veh_list .delete').click(function () {
        console.log('delete');
        var index = get_click_item_index($(this));
        console.log(index);
        //remove element
        $(this).parent().parent().remove();
        //delete data as well
        input_json.data.splice(index,1);
    });
}

function get_click_item_index(element) {
    var id = element.parent().parent().attr('data-id');
    for(var i = 1; i < input_json.data.length; i++) {
        if (input_json.data[i][0] === id) return i;
    }
    return -1;
}

//gantt chart related
var gantt_initilaized = false;

var demo_tasks = {
    "data":[
        {"id":11, "text":"Project #1", "start_date":"28-03-2018", "duration":"11", "progress": 0.6, "open": true},
        {"id":1, "text":"Project #2", "start_date":"01-04-2018", "duration":"18", "progress": 0.4, "open": true},
        {"id":2, "text":"Task #1", "start_date":"02-04-2018", "duration":"8", "parent":"1", "progress":0.5, "open": true},
        {"id":3, "text":"Task #2", "start_date":"11-04-2018", "duration":"8", "parent":"1", "progress": 0.6, "open": true},
        {"id":4, "text":"Task #3", "start_date":"13-04-2018", "duration":"6", "parent":"1", "progress": 0.5, "open": true},
        {"id":5, "text":"Task #1.1", "start_date":"02-04-2018", "duration":"7", "parent":"2", "progress": 0.6, "open": true},
        {"id":6, "text":"Task #1.2", "start_date":"03-04-2018", "duration":"7", "parent":"2", "progress": 0.6, "open": true},
        {"id":7, "text":"Task #2.1", "start_date":"11-04-2018", "duration":"8", "parent":"3", "progress": 0.6, "open": true},
        {"id":8, "text":"Task #3.1", "start_date":"14-04-2018", "duration":"5", "parent":"4", "progress": 0.5, "open": true},
        {"id":9, "text":"Task #3.2", "start_date":"14-04-2018", "duration":"4", "parent":"4", "progress": 0.5, "open": true},
        {"id":10, "text":"Task #3.3", "start_date":"14-04-2018", "duration":"3", "parent":"4", "progress": 0.5, "open": true},

        {"id":12, "text":"Task #1", "start_date":"03-04-2018", "duration":"5", "parent":"11", "progress": 1, "open": true},
        {"id":13, "text":"Task #2", "start_date":"02-04-2018", "duration":"7", "parent":"11", "progress": 0.5, "open": true},
        {"id":14, "text":"Task #3", "start_date":"02-04-2018", "duration":"6", "parent":"11", "progress": 0.8, "open": true},
        {"id":15, "text":"Task #4", "start_date":"02-04-2018", "duration":"5", "parent":"11", "progress": 0.2, "open": true},
        {"id":16, "text":"Task #5", "start_date":"02-04-2018", "duration":"7", "parent":"11", "progress": 0, "open": true},

        {"id":17, "text":"Task #2.1", "start_date":"03-04-2018", "duration":"2", "parent":"13", "progress": 1, "open": true},
        {"id":18, "text":"Task #2.2", "start_date":"06-04-2018", "duration":"3", "parent":"13", "progress": 0.8, "open": true},
        {"id":19, "text":"Task #2.3", "start_date":"10-04-2018", "duration":"4", "parent":"13", "progress": 0.2, "open": true},
        {"id":20, "text":"Task #2.4", "start_date":"10-04-2018", "duration":"4", "parent":"13", "progress": 0, "open": true},
        {"id":21, "text":"Task #4.1", "start_date":"03-04-2018", "duration":"4", "parent":"15", "progress": 0.5, "open": true},
        {"id":22, "text":"Task #4.2", "start_date":"03-04-2018", "duration":"4", "parent":"15", "progress": 0.1, "open": true},
        {"id":23, "text":"Task #4.3", "start_date":"03-04-2018", "duration":"5", "parent":"15", "progress": 0, "open": true}
    ],
    "links":[
        {"id":"1","source":"1","target":"2","type":"1"},
        {"id":"2","source":"2","target":"3","type":"0"},
        {"id":"3","source":"3","target":"4","type":"0"},
        {"id":"4","source":"2","target":"5","type":"2"},
        {"id":"5","source":"2","target":"6","type":"2"},
        {"id":"6","source":"3","target":"7","type":"2"},
        {"id":"7","source":"4","target":"8","type":"2"},
        {"id":"8","source":"4","target":"9","type":"2"},
        {"id":"9","source":"4","target":"10","type":"2"},
        {"id":"10","source":"11","target":"12","type":"1"},
        {"id":"11","source":"11","target":"13","type":"1"},
        {"id":"12","source":"11","target":"14","type":"1"},
        {"id":"13","source":"11","target":"15","type":"1"},
        {"id":"14","source":"11","target":"16","type":"1"},
        {"id":"15","source":"13","target":"17","type":"1"},
        {"id":"16","source":"17","target":"18","type":"0"},
        {"id":"17","source":"18","target":"19","type":"0"},
        {"id":"18","source":"19","target":"20","type":"0"},
        {"id":"19","source":"15","target":"21","type":"2"},
        {"id":"20","source":"15","target":"22","type":"2"},
        {"id":"21","source":"15","target":"23","type":"2"}
    ]
};

var demo_tasks2 = {
    "data":[
        {"id":11, "text":"Project #1", "start_date":"28-03-2018", "duration":"11", "progress": 0.6, "open": true},
        {"id":1, "text":"Project #2", "start_date":"01-04-2018", "duration":"18", "progress": 0.4, "open": true},
        {"id":2, "text":"Task #1", "start_date":"02-04-2018", "duration":"8", "parent":"1", "progress":0.5, "open": true},
        {"id":3, "text":"Task #2", "start_date":"11-04-2018", "duration":"8", "parent":"1", "progress": 0.6, "open": true},
        {"id":4, "text":"Task #3", "start_date":"13-04-2018", "duration":"6", "parent":"1", "progress": 0.5, "open": true},
        {"id":5, "text":"Task #1.1", "start_date":"02-04-2018", "duration":"7", "parent":"2", "progress": 0.6, "open": true},
        {"id":6, "text":"Task #1.2", "start_date":"03-04-2018", "duration":"7", "parent":"2", "progress": 0.6, "open": true},
        {"id":7, "text":"Task #2.1", "start_date":"11-04-2018", "duration":"8", "parent":"3", "progress": 0.6, "open": true},
        {"id":8, "text":"Task #3.1", "start_date":"14-04-2018", "duration":"5", "parent":"4", "progress": 0.5, "open": true},
        {"id":9, "text":"Task #3.2", "start_date":"14-04-2018", "duration":"4", "parent":"4", "progress": 0.5, "open": true},
        {"id":10, "text":"Task #3.3", "start_date":"14-04-2018", "duration":"3", "parent":"4", "progress": 0.5, "open": true},
    ],
    "links":[
    ]
};

var i = 0;

function init() {
    $('#submit').click(function () {
        console.log('submit');
        var submit_csv = Papa.unparse(input_json);
        console.log(submit_csv);
        $('.loading_modal').show();
        $.post('/scheduler', {csv: submit_csv})
            .done(function (data) {
                console.log("Data Loaded: " + data);
                $('.loading_modal').hide();
                $('#form_container').hide();
                $('#gantt_container').show();
                //demo
                var data = i > 0 ? demo_tasks : demo_tasks2;
                draw_gantt(data);
                i++;
            });
    });
    $('#gantt_container .back').click(function () {
        gantt.clearAll();
        $('#gantt_container').hide();
        $('#form_container').show();
    });
}

function draw_gantt(data) {
    gantt_init();
    gantt.parse(data);
}

function gantt_init() {
    if (gantt_initilaized) {
        return;
    }
    gantt.config.readonly = true;
    gantt.config.xml_date = "%d-%m-%Y %H:%i";
    gantt.config.scale_unit = "hour";
    gantt.config.step = 1;
    gantt.config.date_scale = "%g %a";
    gantt.config.min_column_width = 20;
    gantt.config.duration_unit = "minute";
    gantt.config.duration_step = 60;
    gantt.config.scale_height = 75;
    gantt.config.subscales = [
        {unit: "day", step: 1, date: "%j %F, %l"},
        {unit: "minute", step: 15, date: "%i"}
    ];
    gantt.config.columns = [
        {name: "text", tree: true, width: '*', resize: true},
        {name: "start_date", align: "center", resize: true},
        {name: "duration", align: "center"}
    ];
    gantt.templates.scale_cell_class = function (date) {
        if (date.getDay() == 0 || date.getDay() == 6) {
            return "weekend";
        }
    };
    gantt.templates.task_cell_class = function (item, date) {
        if (date.getDay() == 0 || date.getDay() == 6) {
            return "weekend";
        }
    };
    gantt.init("gantt");
    gantt_initilaized = true;
}

init();