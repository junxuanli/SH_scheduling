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

var veh_no_prefix = '';

//form related
var default_input_csv_string = 'Veh_No,SOB,MC101,MC201,MC301,RF101,RF201,RF301,FF101,UB101,BS101,CL100,CL101,CL102,BS201,FI101,FO101,LS101,A metric,B metric,CL201,AS101,BS Audit,C metric,TRANS1,PAINT,TRANS2,T1,T2,WT001,T3,T4,T5,C1,C2,C3,C4,PTI,DR,NF001,DF001,FI001,DC001,LV001,SI001,VFC,ATF,QC001,DVT,QC002,QC003,QC004,CAMO,BLT001,BLT002,WT002,WT003,D metric,RQA,GCA,GLD001,PACK1\n' +
    '1,10/1/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '2,10/5/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '3,10/8/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '4,10/10/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '5,10/11/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0\n' +
    '6,10/12/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,1,0,1,0\n' +
    '7,10/13/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '8,10/14/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,1,0,1,1\n' +
    '9,10/15/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '10,10/16/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '11,10/17/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '12,10/18/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '13,10/19/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '14,10/20/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '15,10/21/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0\n' +
    '16,10/22/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '17,10/23/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0\n' +
    '18,10/24/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1\n' +
    '19,10/25/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1\n' +
    '20,10/26/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,1\n' +
    '21,10/27/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,1,0,1,1\n' +
    '22,10/28/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '23,10/29/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0\n' +
    '24,10/30/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0\n' +
    '25,10/31/2018 8:30,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,1,0';

var input_json = Papa.parse(default_input_csv_string);
console.log(input_json);

var veh_list = $('#form_container #veh_list');
var veh_item_template = '<tr data-id="{0}">\n' +
    '            <th scope="row">{1}</th>\n' +
    '            <td>{2}</td>\n' +
    '            <td>{3}</td>\n' +
    '            <td>\n' +
    '                <button type="button" class="btn btn-link btn-sm edit" data-val="edit" data-toggle="modal" data-target="#formModal">编辑</button>\n' +
    '                <button type="button" class="btn btn-link btn-sm delete">删除</button>\n' +
    '            </td>\n' +
    '        </tr>';

var form_option_item_template = '<div class="row {0}">\n' +
    '                            <label class="col-4">{1}</label>\n' +
    '                            <div class="col-4">\n' +
    '                                <div class="form-check">\n' +
    '                                    <label class="form-check-label">\n' +
    '                                        <input class="form-check-input" type="checkbox" {2} value="1"> 选择任务\n' +
    '                                    </label>\n' +
    '                                </div>\n' +
    '                            </div>\n' +
    '                            <div class="col-4">\n' +
    '                                <div class="form-check">\n' +
    '                                    <label class="form-check-label">\n' +
    '                                        <input class="form-check-input" type="checkbox" {3} value="1"> 任务完成\n' +
    '                                    </label>\n' +
    '                                </div>\n' +
    '                            </div>\n' +
    '                        </div>';

var option_text_item_templates = ['<del>{0}</del> ', '<span>{0}</span> '];

render_veh_list(input_json);
bind_edit_del_events();
form_modal_events();
function render_veh_list(json) {
    for(var i = 1; i < json.data.length; i++) {
        append_to_veh_list(json.data[i]);
    }
}

function append_to_veh_list(data) {
    veh_list.append(String.format(veh_item_template, data[0], veh_no_prefix + data[0], data[1], display_option_text(data)));
}

function update_veh_item(index, data) {
    var item = veh_list.find('tr').eq(index-1);
    item.find('td').eq(0).text(data[1]);
    item.find('td').eq(1).html(display_option_text(data));
}

function display_option_text(data) {
    var options = input_json.data[0];
    var text = '';
    for (var i = 2; i < options.length; i++) {
        text += String.format(option_text_item_templates[data[i]], options[i]);
    }
    return text;
}

function bind_edit_del_events() {
    $('#form_container #veh_list .edit').off('click');
    $('#form_container #veh_list .edit').click(function () {
        console.log('edit');
        console.log(get_click_item_index($(this)));
    });
    $('#form_container #veh_list .delete').off('click');
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

function form_modal_events() {
    $('#formModal').on('show.bs.modal', function (event) {
        console.log($(event.relatedTarget));
        var myVal = $(event.relatedTarget).data('val');
        var index = get_click_item_index($(event.relatedTarget));
        build_form(index);
        $(this).find(".modal-title").text(myVal.toUpperCase());
    });
    $('#formModal .modal-footer .save').click(function () {
        //get index
        var index = $('#formModal .index input').val();
        var veh_no = $('#formModal .veh_no input').val().slice(veh_no_prefix.length);
        var firstday = moment($('#formModal .firstday input').val()).format('MM/D/YYYY HH:mm'); //10/1/2018 8:30
        var data = [veh_no, firstday];
        console.log(index);
        $('#formModal .options .row').each(function (index, element) {
            var val = 1;
            var selected = $(element).find('input').eq(0).prop('checked');
            //completed?
            var completed = $(element).find('input').eq(1).prop('checked');
            if(completed || !selected) {
                val = 0;
            }
            data.push(val);
        });
        console.log(data);
        if (index > 0) {
            //update
            input_json.data[index] = data;
            update_veh_item(index, data);
        } else {
            //insert
            input_json.data.push(data);
            append_to_veh_list(data);
            bind_edit_del_events();
        }
        $('#formModal').modal('toggle');
    });
}

function build_form(index) {
    // $('#formModal .options .biwsob input').eq(1).prop('checked')
    var veh_no, firstday, data;
    if (index >= 0) {
        data = input_json.data[index];
        veh_no = veh_no_prefix + data[0];
        firstday = moment(data[1]).format('YYYY-MM-DDTHH:mm:00');
    } else {
        var veh_id = 1;
        if (input_json.data.length > 1) {
            veh_id = (parseInt(input_json.data[input_json.data.length - 1][0]) + 1);
        }
        veh_no = veh_no_prefix + veh_id;
        firstday = moment().format('YYYY-MM-DDTHH:mm:00'); //2011-08-19T13:45:00
    }
    $('#formModal .index input').val(index);
    $('#formModal .veh_no input').val(veh_no);
    $('#formModal .firstday input').val(firstday);
    var options = $('#formModal .options');
    options.empty();
    var attributes = input_json.data[0];
    for (var i = 2; i < attributes.length; i++) {
        var checked = isChecked(data, i);
        options.append(String.format(form_option_item_template, attributes[i].toLowerCase(), attributes[i], checked, ''));
    }
}

function isChecked(data, index) {
    if (!data) {
        return 'checked';
    }
    return data[index] > 0 ? 'checked' : '';
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
        var dt = moment($('#start-dt-input').val()).format('MM/D/YYYY HH:mm');
        console.log(submit_csv);
        $('.loading_modal').show();
        $.post('/scheduler', {dt: dt, csv: submit_csv})
            .done(function (data) {
                console.log("Data Loaded: " + data);
                var gantt_data = parse_csv_data(data);
                $('.loading_modal').hide();
                $('#form_container').hide();
                $('#gantt_container').show();
                draw_gantt(gantt_data);
            }).fail(function() {
                $('.loading_modal').hide();
                alert( "error" );
            });
    });
    $('#gantt_container .back').click(function () {
        gantt.clearAll();
        $('#gantt_container').hide();
        $('#form_container').show();
    });

    $('#gantt_container input[name=inlineRadioOptions]').click(function () {
        setScaleConfig($(this).val());
        gantt.render();
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

function setScaleConfig(value) {
    switch (value) {
        case "0.5":
            gantt.config.scale_unit = "hour";
            gantt.config.step = 1;
            gantt.config.date_scale = "%H";
            gantt.config.scale_height = 75;
            gantt.config.subscales = [
                {unit: "day", step: 1, date: "%M%j日, %l"},
                {unit: "minute", step: 30, date: "%i"}
            ];
            break;
        case "4":
            gantt.config.scale_unit = "day";
            gantt.config.step = 1;
            gantt.config.date_scale = "%M%j日";
            gantt.config.scale_height = 50;
            gantt.config.subscales = [
                {unit: "hour", step: 4, date: "%H"}
            ];
            gantt.templates.date_scale = null;
            break;
        case "24":
            gantt.config.scale_unit = "day";
            gantt.config.step = 1;
            gantt.config.date_scale = "%M%j日";
            gantt.config.scale_height = 50;
            gantt.config.subscales = [
                {unit: "hour", step: 8, date: "%H"}
            ];
            gantt.templates.date_scale = null;
            break;
    }
}

function gantt_init() {
    if (gantt_initilaized) {
        return;
    }
    gantt.config.readonly = true;
    gantt.config.xml_date = "%Y-%m-%d %H:%i:%s";
    gantt.config.min_column_width = 20;
    gantt.config.duration_unit = "minute";
    gantt.config.duration_step = 1;
    // gantt.config.row_height = 22;
    // gantt.config.static_background = true;
    setScaleConfig('0.5');
    gantt.config.columns = [
        {name: "text", label: "任务", tree: true, width: '*', resize: true},
        {name: "start_date", label: "开始时间", align: "left", width: 100, resize: true, template:function(obj){
                return moment(obj.start_date).format('YY-MM-DD hh:mm');
        }},
        {name: "duration", label: "自然用时", align: "right"}
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
        return "<b>任务:</b> "+task.text+"<br/><b>开始时间:</b> " +
            moment(start).format('YYYY-MM-DD hh:mm')+
            "<br/><b>结束时间:</b> "+moment(end).format('YYYY-MM-DD hh:mm');
    };
    gantt.ignore_time = function (date) {
        if (date.getDay() == 0 || date.getDay() == 6)
            return true;
        if (date.getHours() < 8 || date.getHours() > 16)
            return true;

        return false;
    };
    gantt.init("gantt");
    gantt_initilaized = true;
}

init();