$(document).ready(function() {

    // Undo Hover
    $("#fetch").on('mouseover', '.icon-close2', function() {
        $(this).tooltip({
            title: "Restore This Event!",
            placement: "right"
        });
    });

    // Delete Permanently Hover
    $("#fetch").on('mouseover', '.icon-trash-alt', function() {
        $(this).tooltip({
            title: "Permanently Delete This Event!",
            placement: "right"
        });
    });

    // Undo checked Hover
    $("#fetch").on('mouseover', '.icon-spinner11', function() {
        $(this).tooltip({
            title: "Undo This Event!",
            placement: "right"
        });
    });

    // Make This Event As Done
    $("#fetch").on('mouseover', '.icon-checkmark4', function() {
        $(this).tooltip({
            title: "Make This As Done!",
            placement: "right"
        });
    });

    // Update This Event
    $("#fetch").on('mouseover', '.icon-cursor', function() {
        $(this).tooltip({
            title: "Update This Event!",
            placement: "right"
        });
    });

    // Delete This Event
    $("#fetch").on('mouseover', '.icon-bin2', function() {
        $(this).tooltip({
            title: "Delete This Event!",
            placement: "right"
        });
    });


    $('#date,#dateU').datepicker({
        todayBtn: 'linked',
        format: "yyyy-mm-dd",
        autoclose: true,
        todayHighlight: true,
        startDate: currrent_date()
    });

    $('#filter').datepicker({
        todayBtn: 'linked',
        format: "yyyy-mm-dd",
        autoclose: true
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    })


    let $pagination = $('#pagination'),
        totalRecords = 0,
        records = [],
        displayRecords = [],
        recPerPage = 8,
        page = 1,
        totalPages = 0;

    Build("");

    function Build(date) {
        if (!date) {
            date = "";
        }

        $.ajax({
            url: "/administrateur/toDo/Fetch",
            dataType: 'json',
            data: JSON.stringify({
                "date": date
            }),
            contentType: 'application/json;charset=UTF-8',
            cache: false,
            type: 'post',
            success: function(data) {
                generate_data(data);
            }
        });
    }

    // Generate Events
    function generate_table() {
        $('#fetch').html('');
        const options = {
            year: "numeric",
            month: "long",
            day: "numeric"
        };
        let appendToResult = "";
        for (var i = 0; i < displayRecords.length; i++) {
            const date = new Intl.DateTimeFormat('en', options).format(new Date(displayRecords[i].Date));
            let htmlStr = "<li class='feed-item' id='" + displayRecords[i].Date + "' name='" + displayRecords[i].Id + "'>";

            if (displayRecords[i].Deleted === 0) {
                htmlStr += "</i><i class='icon-close2' style='margin-right:5px;' id='" + displayRecords[i].Id + "'></i>" +
                    "</i><i class='icon-trash-alt' id='" + displayRecords[i].Id + "'></i></div>";
            } else {
                if (displayRecords[i].Seen === 0) {
                    htmlStr += "<span class='date done'>" + date + "</span>" +
                        "<span class='activity-text done'>" + displayRecords[i].Description + "</span>" +
                        "<div class='tools'>" +
                        "<i class='icon-spinner11' id='" + displayRecords[i].Id + "' style='margin-right:5px;'>";
                } else {
                    htmlStr += "<span class='date'>" + date + "</span>" +
                        "<span class='activity-text'>" + displayRecords[i].Description + "</span>" +
                        "<div class='tools'>" +
                        "<i class='icon-checkmark4' id='" + displayRecords[i].Id + "' style='margin-right:5px;'>";
                }
                htmlStr += "</i><i class='icon-bin2' style='margin-right:5px;' id='" + displayRecords[i].Id + "'></i>";
                htmlStr += "<i class='icon-cursor'  id='" + displayRecords[i].Id + "'></i></div></li>";

            }

            appendToResult = appendToResult.concat(htmlStr);
        }
        $('#fetch').append(appendToResult);
    }

    // Generate Pagination
    function apply_pagination() {
        $pagination.twbsPagination({
            totalPages: totalPages,
            visiblePages: 6,
            onPageClick: function(event, page) {
                displayRecordsIndex = Math.max(page - 1, 0) * recPerPage;
                endRec = (displayRecordsIndex) + recPerPage;
                displayRecords = records.slice(displayRecordsIndex, endRec);
                generate_table();
            }
        });
    }
    
    // Generate Loader
    function generate_loader() {
        $('#fetch').html('');
        let appendToResult = "";
        for (var i = 0; i < 7; i++) {
            appendToResult = appendToResult.concat(`
            <div class='ph-item'>
            <div><div class='ph-row'>
            <div class='ph-col-8 empty'></div>
            <div class='ph-col-6'></div>
            <div class='ph-col-6 empty'></div>
            <div class='ph-col-12'></div>
            <div class='ph-col-10 empty'></div>
            </div></div></div>`);
        }
        $('#fetch').append(appendToResult)
    }

    // fetch Single
    $("#fetch").on('click', '.icon-cursor', function() {
        $(this).tooltip('hide');
        const id = $(this).attr("id");
        $.ajax({
            url: "/administrateur/toDo/FetchSingle",
            dataType: 'json',
            data: JSON.stringify({
                "id": id
            }),
            contentType: 'application/json;charset=UTF-8',
            cache: false,
            type: 'post',
            success: function(data, textStatus, xhr) {
                const status = xhr.status;
                if (status === 200) {
                    $('#listU').val(data[0].Description);
                    $('#dateU').val(data[0].Date);
                    $('#event_id').val(data[0].Id);
                    $('#update').modal('toggle');
                } else if (status === 201) {
                    error(data["data"].Msg);
                }
            }
        });
    });

    // Mark As Done
    $("#fetch").on("click", ".icon-checkmark4", function() {
        $(this).tooltip('hide');
        const id = $(this).attr("id");
        const date = date_egality($(this).closest('li').attr('id'));
        if (id !== '') {
            $.ajax({
                url: "/administrateur/toDo/MarkAsDone",
                dataType: 'json',
                data: JSON.stringify({
                    "id": id
                }),
                contentType: 'application/json;charset=UTF-8',
                cache: false,
                type: 'post',
                success: function(data, textStatus, xhr) {
                    const status = xhr.status;
                    if (status === 200) {
                        Build(date);
                    } else if (status === 201) {
                        error(data["data"].Msg);
                    } else if (status === 202) {
                        warning(data["data"].Msg);
                    }
                }
            });
        }
    });


    // Mark As UnDone
    $("#fetch").on("click", ".icon-spinner11", function() {
        $(this).tooltip('hide');
        const id = $(this).attr("id");
        const date = date_egality($(this).closest('li').attr('id'));
        if (id !== '') {
            $.ajax({
                url: "/administrateur/toDo/MarkAsUndone",
                dataType: 'json',
                data: JSON.stringify({
                    "id": id
                }),
                contentType: 'application/json;charset=UTF-8',
                cache: false,
                type: 'post',
                success: function(data, textStatus, xhr) {
                    const status = xhr.status;
                    if (status === 200) {
                        Build(date);
                    } else if (status === 201) {
                        error(data["data"].Msg);
                    } else if (status === 202) {
                        warning(data["data"].Msg);
                    }
                }
            });
        }
    });

    // Delete - Then Undo appears
    $("#fetch").on("click", ".icon-bin2", function() {
        $(this).tooltip('hide');
        const id = $(this).attr("id");
        const date = date_egality($(this).closest('li').attr('id'));
        if (id !== '') {
            $.ajax({
                url: "/administrateur/toDo/PreDelete",
                dataType: 'json',
                data: JSON.stringify({
                    "id": id
                }),
                contentType: 'application/json;charset=UTF-8',
                cache: false,
                type: 'post',
                success: function(data, textStatus, xhr) {
                    const status = xhr.status;
                    if (status === 200) {
                        Build(date);
                    } else if (status === 201) {
                        error(data["data"].Msg);
                    } else if (status === 202) {
                        warning(data["data"].Msg);
                    }
                }
            });
        }
    });

    // delete Permanently
    $("#fetch").on("click", ".icon-trash-alt", function() {
        $(this).tooltip('hide');
        const id = $(this).attr("id");
        const date = date_egality($(this).closest('li').attr('id'));
        if (id !== '') {
            $.ajax({
                url: "/administrateur/toDo/Delete",
                dataType: 'json',
                data: JSON.stringify({
                    "id": id
                }),
                contentType: 'application/json;charset=UTF-8',
                cache: false,
                type: 'post',
                success: function(data, textStatus, xhr) {
                    const status = xhr.status;
                    if (status === 200) {
                        Build(date);
                    } else if (status === 201) {
                        error(data["data"].Msg);
                    } else if (status === 202) {
                        warning(data["data"].Msg);
                    }
                }
            });
        }
    });

    // Undo Delete
    $("#fetch").on("click", ".icon-close2", function() {
        $(this).tooltip('hide');
        const id = $(this).attr("id");
        const date = date_egality($(this).closest('li').attr('id'));
        if (id !== '') {
            $.ajax({
                url: "/administrateur/toDo/Restore",
                dataType: 'json',
                data: JSON.stringify({
                    "id": id
                }),
                contentType: 'application/json;charset=UTF-8',
                cache: false,
                type: 'post',
                success: function(data, textStatus, xhr) {
                    const status = xhr.status;
                    if (status === 200) {
                        Build(date);
                    } else if (status === 201) {
                        error(data["data"].Msg);
                    } else if (status === 202) {
                        warning(data["data"].Msg);
                    }
                }
            });
        }
    });

    // Add An Event
    $("#myForm").submit(function(e) {
        e.preventDefault();
        e.stopPropagation();
        const $list = $("#list");
        const $date = $("#date");
        const $ErrDate = $("#ErrDate span");
        const $ErrTask = $("#ErrTask span");
        $ErrDate.text("");
        $ErrTask.text("");
        const $classDate = $date.attr('class');
        const $classTask = $list.attr('class');
        if ($classDate === "form-control is-invalid") {
            $date.removeClass('form-control is-invalid').addClass('form-control');
        }
        if ($classTask === "form-control is-invalid") {
            $list.removeClass('form-control is-invalid').addClass('form-control');
        }
        $.ajax({
            url: "/administrateur/toDo/Add",
            contentType: "application/x-www-form-urlencoded;charset=utf-8",
            type: 'post',
            cache: false,
            data: $("#myForm").serialize(),
            dataType: 'json',
            success: function(data, textStatus, xhr) {
                const status = xhr.status;
                $("#myForm").trigger("reset");
                if (status === 200) {
                    success(data["data"].Msg);
                    $list.val("");
                    $date.datepicker('setDate', null);
                    $('#form').modal('hide');
                    Build('');
                } else if (status === 201) {
                    let lgTask = 0;
                    let lgDate = 0;
                    let str = "";
                    if (data["data"].Task) {
                        lgTask = data["data"].Task.length;
                    }
                    if (data["data"].Date) {
                        lgDate = data["data"].Date.length;
                    }
                    for (var i = 0; i < lgDate; i++) {
                        str += data["data"].Date[i] + "\n";
                        $date.removeClass('form-control').addClass('form-control is-invalid');
                    }
                    $ErrDate.append(str);
                    str = "";
                    for (var i = 0; i < lgTask; i++) {
                        str += data["data"].Task[i] + "\n";
                        $list.removeClass('form-control').addClass('form-control is-invalid');
                    }
                    $ErrTask.append(str);
                } else if (status === 202) {
                    error(data["data"].Msg);
                }
            }
        });

    });

    // Update An Event
    $("#myFormUpdate").submit(function(e) {
        e.preventDefault();
        e.stopPropagation();
        const $list = $("#listU");
        const $date = $("#dateU");
        const $ErrDate = $("#ErrDateU span");
        const $ErrTask = $("#ErrTaskU span");
        $ErrDate.text("");
        $ErrTask.text("");
        const $classDate = $date.attr('class');
        const $classTask = $list.attr('class');
        if ($classDate === "form-control is-invalid") {
            $date.removeClass('form-control is-invalid').addClass('form-control');
        }
        if ($classTask === "form-control is-invalid") {
            $list.removeClass('form-control is-invalid').addClass('form-control');
        }
        $.ajax({
            url: "/administrateur/toDo/UpdateToDO",
            contentType: "application/x-www-form-urlencoded;charset=utf-8",
            type: 'post',
            cache: false,
            data: $("#myFormUpdate").serialize(),
            dataType: 'json',
            success: function(data, textStatus, xhr) {
                const status = xhr.status;
                $("#myFormUpdate").trigger("reset");
                if (status === 200) {
                    success(data["data"].Msg);
                    $date.datepicker('setDate', null);
                    $('#update').modal('hide');
                    Build('');
                } else if (status === 201) {
                    let lgTask = 0;
                    let lgDate = 0;
                    let str = "";
                    if (data["data"].Task) {
                        lgTask = data["data"].Task.length;
                    }
                    if (data["data"].Date) {
                        lgDate = data["data"].Date.length;
                    }
                    for (var i = 0; i < lgDate; i++) {
                        str += data["data"].Date[i] + "\n";
                        $date.removeClass('form-control').addClass('form-control is-invalid');
                    }
                    $ErrDate.append(str);
                    str = "";
                    for (var i = 0; i < lgTask; i++) {
                        str += data["data"].Task[i] + "\n";
                        $list.removeClass('form-control').addClass('form-control is-invalid');
                    }
                    $ErrTask.append(str);
                } else if (status === 202) {
                    error(data["data"].Msg);
                }
            }
        });

    });

    function generate_data(data) {
        $pagination.twbsPagination('destroy');
        $("#fetch").empty();
        records = data;
        totalRecords = records.length;
        if (data.length === 0) {
            totalPages = 1;
            generate_loader();
            setTimeout(function() {
                $("#fetch").html("<h4 class='h4 text-center' style='padding:160px 0;'>Oops! There is No Event Found!</h4>");
                $("#pagination").html(`
                <li class="page-item first disabled"><a href="#" class="page-link">First</a></li>
                <li class="page-item prev disabled"><a href="#" class="page-link">Previous</a></li>
                <li class="page-item active"><a href="#" class="page-link">1</a></li>
                <li class="page-item next disabled"><a href="#" class="page-link">Next</a></li>
                <li class="page-item last disabled"><a href="#" class="page-link">Last</a></li>`);
            }, 250);
        } else {
            totalPages = Math.ceil(totalRecords / recPerPage);
            generate_loader();
            setTimeout(apply_pagination, 250);
        }
    }

    // Filter Form
    $("#btn").click(function(e) {
        e.preventDefault();
        e.stopPropagation();
        const date = date_egality($("#filter").val());
        $('#filter').datepicker('setDate', null);
        Build(date);
    });

    function date_egality(x) {
        let c = "";
        const date = currrent_date();
        if (x) {
            if (x < date) {
                c = x
            }
        }
        return c;
    }
});