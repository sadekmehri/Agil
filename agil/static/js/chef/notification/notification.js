$(window).scroll(function() {
    if ($(this).scrollTop() > 50) {
        $('#back-to-top').fadeIn(200);
    } else {
        $('#back-to-top').fadeOut(200);
    }
});

$('#back-to-top').click(function() {
    $('body,html').animate({
        scrollTop: 0
    }, 800);
    return false;
});

$(function() {
    $("#notifications").scroll(function() {
        if ($("#Notif").height() <= $("#notifications").height() + $("#notifications").scrollTop()) {
            const id = $("#Notif li").length;
            if (id) {
                loadNotification(id);
            }
        }
    });
});

loadNotification(5);

// Load data Count
function loadNotificationCount() {
    $.ajax({
        url: '/chef/notification/count',
        type: 'post',
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        dataType: 'json',
        success: function(data, textStatus, xhr) {
            const status = xhr.status;
            if (status === 200) {
                $("#nbr").html(data["data"].Msg);
            }
        }
    });
}

// Load All Data
function loadNotification(id) {
    if (!id) {
        id = 0;
    }
    $.ajax({
        url: '/chef/notification/fetch',
        type: 'post',
        data: {
            id: id
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        dataType: 'json',
        beforeSend: function() {
            $('.ajax-loader').show();
        },
        success: function(data, textStatus, xhr) {
            const status = xhr.status;
            if (status === 200) {
                setTimeout(function() {
                    $('.ajax-loader').hide();
                    loadNotificationCount();
                    generate_data_notification(data);
                }, 500);
            } else if (status === 201) {
                error(data["data"].Msg);
                $('.ajax-loader').hide();
            }
        }
    });
}

function generate_data_notification(displayRecords) {
    const lg = displayRecords.length;
    $('#Notif').html("");
    let appendToResult = "";
    let htmlStr = "";
    if (lg === 0) {
        htmlStr = `
        <li class="media">
           <span class="text-muted text-center" style="padding: 95px;">There is No Record</span>
         </li>`;
        appendToResult = appendToResult.concat(htmlStr);
    } else {
        var style = "";
        for (var i = 0; i < lg; i++) {
            if (displayRecords[i].Seen === 1) {
                style = "background-color: #E6E6FA;"
            }
            htmlStr = `
        <li class="media" style="${style}" id="${displayRecords[i].Id}">
         <div class="mr-3 position-relative">
         <img src="/static/photo/alert.png" width="36" height="36" class="rounded" alt="">
         </div>
         <div class="media-body">
         <div class="media-title">
         <a href="#" id="${displayRecords[i].Id}">
         <span class="font-weight-semibold" id="${displayRecords[i].Id}">${displayRecords[i].Titre}</span>
         <span class="text-muted float-right font-size-sm">${displayRecords[i].Date}</span>
         </a>
         </div>
         <span class="text-muted">${displayRecords[i].Description}</span>
         <a href="#"><i id="${displayRecords[i].Id}" hidden class="icon-cross3" style=" float: right;" aria-hidden="true"></i></a>
         </div>
         </li>`;
            appendToResult = appendToResult.concat(htmlStr);
        }
    }
    $('#Notif').append(appendToResult);
}
// Delete One
$("#Notif").on("click", ".icon-cross3", function(e) {
    e.preventDefault();
    let id = $(this).attr("id");
    if (!id) {
        id = 1;
    }
    $.ajax({
        type: "POST",
        data: {
            id: id
        },
        url: '/chef/notification/delete',
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        dataType: 'json',
        beforeSend: function() {
            $('.ajax-loader').show();
        },
        success: function(data, textStatus, xhr) {
            const status = xhr.status;
            if (status === 200) {
                success(data["data"].Msg);
                loadNotification($("#Notif li").length);
            } else if (status === 201) {
                error(data["data"].Msg);
            }
            $('.ajax-loader').hide();
        }
    });
});

//  Mark One as Read
$("#Notif").on("click", ".font-weight-semibold", function(e) {
    e.preventDefault();
    let id = $(this).attr("id");
    if (!id) {
        id = 0;
    }
    $.ajax({
        type: "POST",
        data: {
            id: id
        },
        url: '/chef/notification/seen',
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        dataType: 'json',
        beforeSend: function() {
            $('.ajax-loader').show();
        },
        success: function(data, textStatus, xhr) {
            const status = xhr.status;
            if (status === 200) {
                success(data["data"].Msg);
                loadNotification($("#Notif li").length);
            } else if (status === 201) {
                error(data["data"].Msg);
            }
            $('.ajax-loader').hide();
        }
    });
});

// Mark All as Read
$(".icon-radio-unchecked").on("click", function(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: '/chef/notification/done',
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        dataType: 'json',
        beforeSend: function() {
            $('.ajax-loader').show();
        },
        success: function(data, textStatus, xhr) {
            const status = xhr.status;
            if (status === 200) {
                success(data["data"].Msg);
                loadNotification($("#Notif li").length);
            } else if (status === 201) {
                error(data["data"].Msg);
            }
            $('.ajax-loader').hide();
        }
    });
});

// Delete All
$(".icon-checkmark3").on("click", function(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: '/chef/notification/deleteAll',
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        dataType: 'json',
        beforeSend: function() {
            $('.ajax-loader').show();
        },
        success: function(data, textStatus, xhr) {
            const status = xhr.status;
            if (status === 200) {
                success(data["data"].Msg);
                loadNotification($("#Notif li").length);
            } else if (status === 201) {
                error(data["data"].Msg);
            }
            $('.ajax-loader').hide();
        }
    });
});

$("#Notif").on("mouseover", ".media", function() {
    $(this).find('.icon-cross3').attr('hidden', false).fadeIn(500);
});

$("#Notif").on("mouseout", ".media", function() {
    $(this).find('.icon-cross3').attr('hidden', true).fadeOut(500);
});