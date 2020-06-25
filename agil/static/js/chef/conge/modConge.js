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

    FecthEmployee($('#Code').val());

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
});