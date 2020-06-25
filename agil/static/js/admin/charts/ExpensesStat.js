var myNewChart4;
$('#daterange-ranges4').daterangepicker({
       startDate: moment().subtract(29, 'days'),
       endDate: moment(),
       minDate: '2020-01-01',
       maxDate: currrent_date(),
       ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
       },
       opens: $('html').attr('dir') == 'rtl' ? 'right' : 'left',
       applyClass: 'btn-sm btn-success btn-block',
       cancelClass: 'btn-sm btn-danger btn-block',
       locale: {
           format: 'YYYY-MM-DD',
           direction: $('html').attr('dir') == 'rtl' ? 'rtl' : 'ltr'
       }
   },
   function(start, end) {
       $('#daterange-ranges4 span').html(start.format('MMMM D') + ' - ' + end.format('MMMM D'));
        startDate = start.format('YYYY-MM-DD');
        endDate = end.format('YYYY-MM-DD');
        $("#loadExpenses").show();
        $("#expenses").hide();
        setTimeout(function () {
            $("#loadExpenses").hide();
            loadExpenses(GetIdStation(),$("#daterange-ranges4").data('daterangepicker').startDate.format('YYYY-MM-DD'),$("#daterange-ranges4").data('daterangepicker').endDate.format('YYYY-MM-DD'));
            $("#expenses").show();
        },1000);
   }
   );
   $('#daterange-ranges4 span').html(moment().subtract(29, 'days').format('MMMM D') + ' - ' + moment().format('MMMM D'));

   setTimeout(function () {
       $("#loadExpenses").hide();
       loadExpenses(GetIdStation(),$("#daterange-ranges4").data('daterangepicker').startDate.format('YYYY-MM-DD'),$("#daterange-ranges4").data('daterangepicker').endDate.format('YYYY-MM-DD'));
       $("#expenses").show();
   },1000);

   function loadExpenses(idStation,startDate,endDate) {
         var don = [];
         var color = [];
         if(!startDate){ startDate = currrent_date();}
         if(!endDate){ endDate = currrent_date();}
         if(!idStation){ idStation = 0;}
       $.ajax({
             url: '/administrateur/station/statistique/expenses',
             type: 'post',
             contentType: "application/x-www-form-urlencoded;charset=utf-8",
             data: {
                 idStation: idStation,startDate:startDate,endDate:endDate
             },
             dataType: 'json',
             success: function(data, textStatus, xhr) {
                 const status = xhr.status;
                 if (status === 200) {
                     const lg = data.length;
                     if (window.myNewChart4 !== undefined)
                         window.myNewChart4.destroy();
                     myNewChart4 = createChartExp();
                     myNewChart4.data.labels.pop();
                     myNewChart4.data.datasets.pop();
                     if (lg > 0) {
                         for (let i = 0; i < lg; i++) {
                             myNewChart4.data.labels.push(data[i].Date);
                             don.push(data[i].Prix);
                             color.push(Tab[Math.floor(Math.random() * Tab.length)]);
                         }
                     }
                      myNewChart4.data.datasets.push({
                          label:"Dépenses totales",
                          data:don,
                          fill:true,
                          backgroundColor:color
                      });
                   myNewChart4.update();
                 }else if(status === 201){
                     error(data["data"].Msg);
                 }
             }
         });
   }
    function createChartExp() {
        const exp = document.getElementById("expenses");
        const ctx_exp = exp.getContext("2d");
        const dat_exp = {
            labels: [],
            datasets: [{
                label: "Dépenses totales",
                data: [],
                fill: false,
                backgroundColor: []
            }]
        };

        return new Chart(ctx_exp, {
            type: "bar",
            data: dat_exp,
            options: {
                title: {
                    display: true,
                    text: 'Dépenses totales par mois'
                },
                legend: {display: false},
                responsive: true,
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                animation: {
                    duration: 1000,
                    xAxis: true,
                    yAxis: true
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: "Dépenses (TND)"
                        }
                    }],
                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: "Mois"
                        }
                    }]
                }
            }
        });
    }
