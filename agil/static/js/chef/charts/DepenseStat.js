    var myNewChart2;
    function currrent_date() {
        const today = new Date();
        const dd = String(today.getDate()).padStart(2, '0');
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const yyyy = today.getFullYear();
        return (yyyy + '-' + mm + '-' + dd);
    }

	// Statistique lavage Begins Here
    function createChartDep() {
        const dep = document.getElementById("dep");
        const ctx_dep = dep.getContext("2d");
        const dat_dep = {
            labels: [],
            datasets: [{
                label: "Depense",
                backgroundColor: "#2a9d8f",
                fillColor: "rgba(220,220,220,0.2)",
                strokeColor: "rgba(220,220,220,1)",
                pointColor: "rgba(220,220,220,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: []
            }]
        };

        return new Chart(ctx_dep, {
            type: "line",
            data: dat_dep,
            options: {
                title: {
                    display: true,
                    text: 'Depense'
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
                            labelString: "Valeur (TND)"
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

   function loadDep(startDate,endDate) {
       var don = [];
       if(!startDate){ startDate = currrent_date();}
       if(!endDate){ endDate = currrent_date();}
       $.ajax({
           url: '/chef/dateDepense',
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
                   if (window.myNewChart2 !== undefined)
                         window.myNewChart2.destroy();
                   myNewChart2 = createChartDep();
                   myNewChart2.data.labels.pop();
                   myNewChart2.data.datasets.pop();
                   if (lg > 0) {
                       for (let i = 0; i < lg; i++) {
                           myNewChart2.data.labels.push(data[i].Date);
                           don.push(data[i].Prix);
                       }
                   }
                   myNewChart2.data.datasets.push({
                       label: "Depense",
                       fill: true,
                       backgroundColor: "#2a9d8f",
                       fillColor: "rgba(220,220,220,0.2)",
                       strokeColor: "rgba(220,220,220,1)",
                       pointColor: "rgba(220,220,220,1)",
                       pointStrokeColor: "#fff",
                       pointHighlightFill: "#fff",
                       pointHighlightStroke: "rgba(220,220,220,1)",
                       data: don,
                   });
                   myNewChart2.update();
               }else if(status === 201){
                   error(data["data"].Msg);
               }
           }
       });
   }

       // Initialize
       $('#daterange-ranges3').daterangepicker(
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
           $('#daterange-ranges3 span').html(start.format('MMMM D') + ' - ' + end.format('MMMM D'));
            startDate = start.format('YYYY-MM-DD');
            endDate = end.format('YYYY-MM-DD');
            $("#loadDep").show();
            $("#dep").hide();
            setTimeout(function () {
                $("#loadDep").hide();
                loadDep($("#daterange-ranges3").data('daterangepicker').startDate.format('YYYY-MM-DD'),$("#daterange-ranges3").data('daterangepicker').endDate.format('YYYY-MM-DD'));
                $("#dep").show();
            },1000);
       }
       );
       $('#daterange-ranges3 span').html(moment().subtract(29, 'days').format('MMMM D') + ' - ' + moment().format('MMMM D'));

       setTimeout(function () {
           $("#loadDep").hide();
           loadDep($("#daterange-ranges3").data('daterangepicker').startDate.format('YYYY-MM-DD'),$("#daterange-ranges3").data('daterangepicker').endDate.format('YYYY-MM-DD'));
           $("#dep").show();
       },1000);
