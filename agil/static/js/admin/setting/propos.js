   $("#Cin,#Tel").inputmask(
      {"mask": '9{8}'}
   );

   $('#Date').datepicker({
      todayBtn: 'linked',
      format: "yyyy-mm-dd",
      autoclose: true,
      todayHighlight: true,
      endDate: currrent_date()
   });

   function currrent_date() {
      const today = new Date();
      const dd = String(today.getDate()).padStart(2, '0');
      const mm = String(today.getMonth() + 1).padStart(2, '0');
      const yyyy = today.getFullYear();
      return (yyyy + '-' + mm + '-' + dd);
   }

   function getDate(date){
      if(!date || !moment(date, 'YYYY-MM-DD',true).isValid()){ date = currrent_date();}
      let dates = new Date(date);
      const dd = String(dates.getDate()).padStart(2, '0');
      const mm = String(dates.getMonth() + 1).padStart(2, '0');
      const yyyy = dates.getFullYear();
      return (yyyy + '-' + mm + '-' + dd);
   }


   $("#btnUpdate").click(function(){
      $("#Code").val($("#codeEmp").text());
      $("#Cin").val($("#cinEmp").text());
      $("#Nom").val($("#nomEmp").text());
      $("#Prenom").val($("#prenomEmp").text());
      $("#Tel").val($("#telEmp").text());
      $("#Email").val($("#emailEmp").text());
      $("#Date").val(getDate($("#dateEmp").text()));
   });