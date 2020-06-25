var myNewChart3;
$('#daterange-ranges3').daterangepicker({
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
       $('#daterange-ranges3 span').html(start.format('MMMM D') + ' - ' + end.format('MMMM D'));
        startDate = start.format('YYYY-MM-DD');
        endDate = end.format('YYYY-MM-DD');
        $("#loadRevenues").show();
        $("#revenues").hide();
        setTimeout(function () {
            $("#loadRevenues").hide();
            loadRevenues(GetIdStation(),$("#daterange-ranges3").data('daterangepicker').startDate.format('YYYY-MM-DD'),$("#daterange-ranges3").data('daterangepicker').endDate.format('YYYY-MM-DD'));
            $("#revenues").show();
        },1000);
   }
   );
   $('#daterange-ranges3 span').html(moment().subtract(29, 'days').format('MMMM D') + ' - ' + moment().format('MMMM D'));

   setTimeout(function () {
       $("#loadRevenues").hide();
       loadRevenues(GetIdStation(),$("#daterange-ranges3").data('daterangepicker').startDate.format('YYYY-MM-DD'),$("#daterange-ranges3").data('daterangepicker').endDate.format('YYYY-MM-DD'));
       $("#revenues").show();
   },1000);

   function loadRevenues(idStation,startDate,endDate) {
         var don = [];
         var color = [];
         if(!startDate){ startDate = currrent_date();}
         if(!endDate){ endDate = currrent_date();}
         if(!idStation){ idStation = 0;}
       $.ajax({
             url: '/administrateur/station/statistique/revenue',
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
                     if (window.myNewChart3 !== undefined)
                         window.myNewChart3.destroy();
                     myNewChart3 = createChartRev();
                     myNewChart3.data.labels.pop();
                     myNewChart3.data.datasets.pop();
                     if (lg > 0) {
                         for (let i = 0; i < lg; i++) {
                             myNewChart3.data.labels.push(data[i].Date);
                             don.push(data[i].Prix);
                             color.push(Tab[Math.floor(Math.random() * Tab.length)]);
                         }
                     }
                      myNewChart3.data.datasets.push({
                          label:"Total des revenus",
                          data:don,
                          fill:true,
                          backgroundColor:color
                      });
                   myNewChart3.update();
                 }else if(status === 201){
                     error(data["data"].Msg);
                 }
             }
         });
   }
    function createChartRev() {
        const rev = document.getElementById("revenues");
        const ctx_rev = rev.getContext("2d");
        const dat_rev = {
            labels: [],
            datasets: [{
                label: "Revenu total",
                data: [],
                fill: false,
                backgroundColor: []
            }]
        };

        return new Chart(ctx_rev, {
            type: "bar",
            data: dat_rev,
            options: {
                title: {
                    display: true,
                    text: 'Total des revenus par mois'
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
                            labelString: "Revenu (TND)"
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