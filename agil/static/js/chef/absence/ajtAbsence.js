$(document).ready(function() {

    $('#Date').datepicker({
        todayBtn: 'linked',
        format: "yyyy-mm-dd",
        autoclose: true,
        endDate: currrent_date()
    });

    function currrent_date() {
        const today = new Date();
        const dd = String(today.getDate()).padStart(2, '0');
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const yyyy = today.getFullYear();
        return (yyyy + '-' + mm + '-' + dd);
    }

    const csrf_token = $("#csrf_token").val();
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    function delay(callback, ms) {
        var timer = 0;
        return function() {
            var context = this,
                args = arguments;
            clearTimeout(timer);
            timer = setTimeout(function() {
                callback.apply(context, args);
            }, ms || 0);
        };
    }

    // Fetch Employee
    $('#Code').keyup(delay(function(e) {
           $("#Name").val("");
           $("#Prenom").val("");
           $("#Groupe").val("");
           FecthEmployee(this.value);
    }, 500));

    function FecthEmployee(id) {
        $.ajax({
            type: 'post',
            url: "/chef/FetchEmp",
            data: {
                id: id
            },
            contentType: "application/x-www-form-urlencoded;charset=ISO-8859-15",
            dataType: 'json',
            success: function(data, textStatus, xhr) {
                var status = xhr.status;
                if (status === 200) {
                    $("#Name").val(data[0].Nom);
                    $("#Prenom").val(data[0].Prenom);
                    $("#Groupe").val(data[0].Groupe);
                    success("Les données d'employé ont été récupérées avec succès");
                }else if(status === 201){
                      error(data["data"].Msg);
                }
            }
        });
    }

    // Absence
    $("#myForm").submit(function(e) {
        e.preventDefault();
        e.stopPropagation();
        const $date = $("#Date");
        const $desc = $("#Desc");
        const $code = $("#Code");
        const $ErrCode = $("#ErrCode span");
        const $ErrDate = $("#ErrDate span");
        const $ErrDesc = $("#ErrDesc span");
        const dates = $date.val();
        $ErrCode.text("");
        $ErrDate.text("");
        $ErrDesc.text("");
        let $classDate = $date.attr('class');
        let $classDesc = $desc.attr('class');
        let $classCode = $code.attr('class');
        if ($classDate === "form-control is-invalid") {
            $date.removeClass('form-control is-invalid').addClass('form-control');
        }
        if ($classDesc === "form-control is-invalid") {
            $desc.removeClass('form-control is-invalid').addClass('form-control');
        }
        if ($classCode === "form-control is-invalid") {
            $code.removeClass('form-control is-invalid').addClass('form-control');
        }
        $.ajax({
            url: "/chef/absence/AddEmp",
            contentType: "application/x-www-form-urlencoded;charset=utf-8",
            type: 'post',
            cache: false,
            data: $("#myForm").serialize(),
            dataType: 'json',
            success: function(data, textStatus, xhr) {
                const status = xhr.status;
                $("#myForm").trigger("reset");
                if (status === 200) {
                    $date.val("");
                    $desc.val("");
                    $code.val("");
                    $date.datepicker('setDate', null);
                    window.location.replace("/chef/absence/consulter?Date="+dates);
                } else if (status === 201) {
                    let lgDesc = 0;
                    let lgDate = 0;
                    let lgCode = 0;
                    let str = "";
                    if (data["data"].Code) {
                        lgCode = data["data"].Code.length;
                    }
                    if (data["data"].Date) {
                        lgDate = data["data"].Date.length;
                    }
                    if (data["data"].Desc) {
                        lgDesc = data["data"].Desc.length;
                    }
                    for (var i = 0; i < lgCode; i++) {
                        str += data["data"].Code[i] + "\n";
                        $code.removeClass('form-control').addClass('form-control is-invalid');
                    }
                    $ErrCode.append(str);
                    str = "";
                    for (var i = 0; i < lgDate; i++) {
                        str += data["data"].Date[i] + "\n";
                        $date.removeClass('form-control').addClass('form-control is-invalid');
                    }
                    $ErrDate.append(str);
                    str = "";
                    for (var i = 0; i < lgDesc; i++) {
                        str += data["data"].Desc[i] + "\n";
                        $desc.removeClass('form-control').addClass('form-control is-invalid');
                    }
                    $ErrDesc.append(str);
                } else if (status === 202) {
                    error(data["data"].Msg);
                }
            }
        });
    });
});