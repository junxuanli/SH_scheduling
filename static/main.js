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

var veh_no_prefix = 'xxx-xxx-x';

//form related
var default_input_csv_string = 'Veh_No,FirstDay,BIWSOB,MC101,MC201,MC301,RF101,RF201,RF301,FF101,UB101,BS101,CL100,CL101,CL102,BS201,FI101,FO101,LS101,A metric,B metric,CL201,AS101,BS Audit,C metric,TRANSSOB,TRANS1,PAINT,TRANS2,GASOB,T1,T2,WT001,T3,T4,T5,C1,C2,C3,C4,PTI,DR,NF001,DF001,FI001,DC001,LV001,SI001,VFC,ATF,QC001,DVT,QC002,QC003,QC004,CAMO,BLT001,BLT002,WT002,WT003,D metric,RQA,GCA,GLD001,VehicleEOB,PACK1\n' +
    '1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '2,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '3,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '4,10,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '5,11,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0\n' +
    '6,12,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,1,0,1,1,0\n' +
    '7,13,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '8,14,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,1,0,1,1,1\n' +
    '9,15,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '10,16,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '11,17,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '12,18,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '13,19,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '14,20,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '15,21,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0\n' +
    '16,22,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '17,23,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0\n' +
    '18,24,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,1\n' +
    '19,25,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,1\n' +
    '20,26,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,1\n' +
    '21,27,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,1,0,1,1,1\n' +
    '22,28,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '23,29,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0\n' +
    '24,30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0\n' +
    '25,31,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1,0';

var input_json = Papa.parse(default_input_csv_string);
console.log(input_json);

var veh_list = $('#form_container #veh_list');
var veh_item_template = '<tr data-id="{0}">\n' +
    '            <th scope="row">{1}</th>\n' +
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
        veh_list.append(String.format(veh_item_template, json.data[i][0], veh_no_prefix + json.data[i][0], json.data[i][1], json.data[i].join('-')));
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

function init() {
    $('#submit').click(function () {
        console.log('submit');
        var submit_csv = Papa.unparse(input_json);
        console.log(submit_csv);
        $('.loading_modal').show();
        $.post('/scheduler', {csv: submit_csv})
            .done(function (data) {
                console.log("Data Loaded: " + data);
                var gantt_data = parse_csv_data(data);
                $('.loading_modal').hide();
                $('#form_container').hide();
                $('#gantt_container').show();
                draw_gantt(gantt_data);
            });
    });
    $('#gantt_container .back').click(function () {
        gantt.clearAll();
        $('#gantt_container').hide();
        $('#form_container').show();
    });
}

function parse_csv_data(data) {
    var json = Papa.parse(data);
    var tasks = {
        "data":[],
        "links":[]
    };
    for(var i = 1; i < json.data.length; i++) {
        var row = json.data[i];
        if (row && row.length > 1) {
            var id = veh_no_prefix + row[0];
            var proj = {"id": id, "text": id, "open": true};
            tasks.data.push(proj);
            for (var j = 1; j < row.length; j++) {
                var task_name = json.data[0][j];
                var content = row[j].split('$');
                if (content[0] != -1) {
                    //2018-10-15 08:30:00
                    var task = {"id": id + task_name, "text": task_name, "start_date": content[0], "duration": content[1], "parent": id};
                    // var task = {"id": id + task_name, "text": task_name, "start_date": "01-04-2018 08:00", "duration": content[1], "parent": id, "progress":0.5, "open": true};
                    tasks.data.push(task);
                }
            }
        }
    }
    console.log(tasks);
    return tasks;
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
    gantt.config.xml_date = "%Y-%m-%d %H:%i:%s";
    gantt.config.scale_unit = "hour";
    gantt.config.step = 1;
    gantt.config.date_scale = "%g %a";
    gantt.config.min_column_width = 20;
    gantt.config.duration_unit = "minute";
    gantt.config.duration_step = 1;
    gantt.config.scale_height = 75;
    // gantt.config.row_height = 22;
    gantt.config.static_background = true;
    gantt.config.subscales = [
        {unit: "day", step: 1, date: "%j %F, %l"},
        {unit: "minute", step: 15, date: "%i"}
    ];
    gantt.config.columns = [
        {name: "text", tree: true, width: '*', resize: true},
        {name: "start_date", align: "left", width: 100, resize: true, template:function(obj){
                return moment(obj.start_date).format('YY-MM-DD hh:mm');
        }},
        {name: "duration", align: "right"}
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
    gantt.templates.tooltip_text = function(start,end,task){
        return "<b>Task:</b> "+task.text+"<br/><b>Start time:</b> " +
            moment(start).format('YYYY-MM-DD hh:mm')+
            "<br/><b>End time:</b> "+moment(end).format('YYYY-MM-DD hh:mm');
    };
    gantt.ignore_time = function (date) {
        if (date.getDay() == 0 || date.getDay() == 6)
            return true;
        if (date.getHours() < 8 || date.getHours() > 18)
            return true;

        return false;
    };
    gantt.init("gantt");
    gantt_initilaized = true;
}

init();