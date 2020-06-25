    var myNewChart1;
    function createChartCarb() {
        // Statistique lavage Begins Here
        const carb = document.getElementById("carb");
        const ctx_carb = carb.getContext("2d");
        const dat_carb = {
            labels: [],
            datasets: [{
                label: "Recette Carburant",
                fill: true,
                backgroundColor: "rgba(168,218,220,1)",
                fillColor: "rgba(220,220,220,0.2)",
                strokeColor: "rgba(220,220,220,1)",
                pointColor: "rgba(220,220,220,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: []
            }]
        };

        return new Chart(ctx_carb, {
            type: "line",
            data: dat_carb,
            options: {
                title: {
                    display: true,
                    text: 'Recette Carburant'
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
                            labelString: "Revenue (TND)"
                        }
                    }],
                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: "Date"
                        }
                    }]
                }
            }
        });
    }

   function loadCarb(startDate,endDate) {
       var don = [];
       if(!startDate){ startDate = currrent_date();}
       if(!endDate){ endDate = currrent_date();}
       $.ajax({
           url: '/chef/dateCarburant',
           type: 'post',
           contentType: "application/x-www-form-urlencoded;charset=utf-8",
           data: {
               startDate:startDate,endDate:endDate
           },
           dataType: 'json',
           success: function(data, textStatus, xhr) {
               var status = xhr.status;
               if (status === 200) {
                   var lg = data.length;
                   if (window.myNewChart1 !== undefined)
                         window.myNewChart1.destroy();
                   myNewChart1 = createChartCarb();
                   myNewChart1.data.labels.pop();
                   myNewChart1.data.datasets.pop();
                   if (lg > 0) {
                       for (let i = 0; i < lg; i++) {
                           myNewChart1.data.labels.push(data[i].Date);
                           don.push(data[i].Prix);
                       }
                   }
                   myNewChart1.data.datasets.push({
                       label: "Recette Carburant",
                       fill: true,
                       backgroundColor: "rgba(168,218,220,1)",
                       fillColor: "rgba(220,220,220,0.2)",
                       strokeColor: "rgba(220,220,220,1)",
                       pointColor: "rgba(220,220,220,1)",
                       pointStrokeColor: "#fff",
                       pointHighlightFill: "#fff",
                       pointHighlightStroke: "rgba(220,220,220,1)",
                       data: don,
                   });
                   myNewChart1.update();
               }else if(status === 201){
                   error(data["data"].Msg);
               }
           }
       });
   }

       // Initialize
       $('#daterange-ranges1').daterangepicker(
       {
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
           $('#daterange-ranges1 span').html(start.format('MMMM D') + ' - ' + end.format('MMMM D'));
            startDate = start.format('YYYY-MM-DD');
            endDate = end.format('YYYY-MM-DD');
            $("#loadCarb").show();
            $("#carb").hide();
            setTimeout(function () {
                $("#loadCarb").hide();
                loadCarb($("#daterange-ranges1").data('daterangepicker').startDate.format('YYYY-MM-DD'),$("#daterange-ranges1").data('daterangepicker').endDate.format('YYYY-MM-DD'));
                $("#carb").show();
            },1000);
       }
       );
       $('#daterange-ranges1 span').html(moment().subtract(29, 'days').format('MMMM D') + ' - ' + moment().format('MMMM D'));

       setTimeout(function () {
           $("#loadCarb").hide();
           loadCarb($("#daterange-ranges1").data('daterangepicker').startDate.format('YYYY-MM-DD'),$("#daterange-ranges1").data('daterangepicker').endDate.format('YYYY-MM-DD'));
           $("#carb").show();
       },1000);
