$(document).ready(function() {

     $('.input-daterange').datepicker({
         todayBtn: 'linked',
         format: 'yyyy-mm-dd',
         autoclose: true
     });

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
        const $dateDeb = $("#DateDeb");
        const $dateFin = $("#DateFin");
        const $desc = $("#Desc");
        const $code = $("#Code");
        const $type = $("#Type");
        const dates = $dateDeb.val();
        const $ErrCode = $("#ErrCode span");
        const $ErrDateDeb = $("#ErrDateDeb span");
        const $ErrDateFin = $("#ErrDateFin span");
        const $ErrDesc = $("#ErrDesc span");
        const $ErrType = $("#ErrType span");
        $ErrCode.text("");
        $ErrDateDeb.text("");
        $ErrDateFin.text("");
        $ErrDesc.text("");
        $ErrType.text("");
        const $classDateDeb = $dateDeb.attr('class');
        const $classDateFin = $dateFin.attr('class');
        const $classDesc = $desc.attr('class');
        const $classCode = $code.attr('class');
        const $classType = $type.attr('class');
        if ($classDateDeb === "form-control is-invalid") {
            $dateDeb.removeClass('form-control is-invalid').addClass('form-control');
        }
        if ($classDateFin === "form-control is-invalid") {
            $dateFin.removeClass('form-control is-invalid').addClass('form-control');
        }
        if ($classCode === "form-control is-invalid") {
            $code.removeClass('form-control is-invalid').addClass('form-control');
        }
        if ($classDesc === "form-control is-invalid") {
            $desc.removeClass('form-control is-invalid').addClass('form-control');
        }
        if ($classType === "form-control is-invalid") {
            $type.removeClass('form-control is-invalid').addClass('form-control');
        }
        $.ajax({
            url: "/chef/conge/AddEmp",
            contentType: "application/x-www-form-urlencoded;charset=utf-8",
            type: 'post',
            cache: false,
            data: $("#myForm").serialize(),
            dataType: 'json',
            success: function(data, textStatus, xhr) {
                var status = xhr.status;
                $("#myForm").trigger("reset");
                if (status === 200) {
                    $desc.val("");
                    $code.val("");
                    $(".input-daterange").datepicker('setDate', null);
                    window.location.replace("/chef/conge?Date="+dates);
                } else if (status === 201) {
                    var lgDesc = 0;
                    var lgType = 0;
                    var lgCode = 0;
                    var lgDateDeb = 0;
                    var lgDateFin = 0;
                    var str = "";
                    if (data["data"].Code) {
                        lgCode = data["data"].Code.length;
                    }
                    if (data["data"].Type) {
                        lgType = data["data"].Type.length;
                    }
                    if (data["data"].DatDeb) {
                        lgDateDeb = data["data"].DatDeb.length;
                    }
                    if (data["data"].DatFin) {
                        lgDateFin = data["data"].DatFin.length;
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
                    for (var i = 0; i < lgType; i++) {
                        str += data["data"].Type[i] + "\n";
                        $type.removeClass('form-control').addClass('form-control is-invalid');
                    }
                    $ErrType.append(str);
                    str = "";
                    for (var i = 0; i < lgDesc; i++) {
                        str += data["data"].Desc[i] + "\n";
                        $desc.removeClass('form-control').addClass('form-control is-invalid');
                    }
                    $ErrDesc.append(str);
                    str = "";
                    for (var i = 0; i < lgDateDeb; i++) {
                        str += data["data"].DatDeb[i] + "\n";
                        $dateDeb.removeClass('form-control').addClass('form-control is-invalid');
                    }
                    $ErrDateDeb.append(str);
                    str = "";
                    for (var i = 0; i < lgDateFin; i++) {
                        str += data["data"].DatFin[i] + "\n";
                        $dateFin.removeClass('form-control').addClass('form-control is-invalid');
                    }
                    $ErrDateFin.append(str);
                } else if (status === 202) {
                    error(data["data"].Msg);
                }
            }
        });
    });
});