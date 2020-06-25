const csrf_token = $("#csrf_token").val();
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

fetchCiterne();
function fetchCiterne(){
    $.ajax({
        type: 'post',
        url: '/chef/CiterneFetch',
        contentType: "application/x-www-form-urlencoded;charset=ISO-8859-15",
        success: function(data, textStatus, xhr) {
            if (xhr.status === 200) {
                var opts = $.parseJSON(data);
                $("#select_citerne").prop('required', true);
                $.each(opts, function(i, d) {
                $('#select_citerne').append('<option value="' + d.Id + '">' + d.NomCit + '</option>');
            });
            }
        }
    });
}

function changeData(id){
    if(!id){id=0;}
      $.ajax({
        type: 'post',
        url: '/chef/CiterneInfo',
         data: JSON.stringify({
             "id": id
        }),
        contentType: 'application/json;charset=UTF-8',
        cache: false,
        success: function(data, textStatus, xhr) {
            if (xhr.status === 200) {
                update($.parseJSON(data));
            }
        }
    });
}

$("#select_citerne").change(function() {
    changeData($(this).val());
});

// Jauge Section
const size = 232;
const min = 0;
const max = 100;
const sliceQty = 5;

const d3Container = d3.select("#citVal"),
    width = size,
    height = (size / 2) + 20,
    radius = (size / 2),
    ringInset = 15,
    ringWidth = 20,

    pointerWidth = 10,
    pointerTailLength = 5,
    pointerHeadLengthPercent = 0.75,

    minValue = min,
    maxValue = max,

    minAngle = -90,
    maxAngle = 90,

    slices = sliceQty,
    range = maxAngle - minAngle,
    pointerHeadLength = Math.round(radius * pointerHeadLengthPercent);

const colors = d3.scale.linear()
    .domain([0, slices - 1])
    .interpolate(d3.interpolateHsl)
    .range(['#66BB6A', '#EF5350']);

const container = d3Container.append('svg');

const svg = container
    .attr('width', width)
    .attr('height', height);

const arc = d3.svg.arc()
    .innerRadius(radius - ringWidth - ringInset)
    .outerRadius(radius - ringInset)
    .startAngle(function (d, i) {
        var ratio = d * i;
        return deg2rad(minAngle + (ratio * range));
    })
    .endAngle(function (d, i) {
        var ratio = d * (i + 1);
        return deg2rad(minAngle + (ratio * range));
    });

const scale = d3.scale.linear()
    .range([0, 1])
    .domain([minValue, maxValue]);

const ticks = scale.ticks(slices);
const tickData = d3.range(slices)
    .map(function () {
        return 1 / slices;
    });

function deg2rad(deg) {
    return deg * Math.PI / 180;
}

function newAngle(d) {
    const ratio = scale(d);
    const newAngle = minAngle + (ratio * range);
    return newAngle;
}

const arcs = svg.append('g')
    .attr('transform', "translate(" + radius + "," + radius + ")")
    .style({
        'stroke': '#fff',
        'stroke-width': 2,
        'shape-rendering': 'crispEdges'
    });

arcs.selectAll('path')
    .data(tickData)
    .enter()
    .append('path')
    .attr('fill', function(d, i) {
        return colors(i);
    })
    .attr('d', arc);

const arcLabels = svg.append('g')
    .attr('transform', "translate(" + radius + "," + radius + ")");

arcLabels.selectAll('text')
    .data(ticks)
    .enter()
    .append('text')
    .attr('transform', function(d) {
        var ratio = scale(d);
        var newAngle = minAngle + (ratio * range);
        return 'rotate(' + newAngle + ') translate(0,' + (10 - radius) + ')';
    })
    .style({
        'text-anchor': 'middle',
        'font-size': 11,
        'fill': '#999'
    })
    .text(function(d) {
        return d + "%";
    });

const lineData = [
    [pointerWidth / 2, 0],
    [0, -pointerHeadLength],
    [-(pointerWidth / 2), 0],
    [0, pointerTailLength],
    [pointerWidth / 2, 0]
];

const pointerLine = d3.svg.line()
    .interpolate('monotone');

const pointerGroup = svg
    .append('g')
    .data([lineData])
    .attr('transform', "translate(" + radius + "," + radius + ")");

pointer = pointerGroup
    .append('path')
    .attr('d', pointerLine)
    .attr('transform', 'rotate(' + minAngle + ')');

function update(data) {
    let valAct = 0;
    let valCiterne = 1;
    if(data) {
        $.each(data, function(i, d) {
             valAct = d.ValAct;
             valCiterne = d.Volume;
        });
    }
    const div = (valAct / valCiterne).toFixed(3);
    $("#avg").text(div * 100 + "%");
    const newAngle = minAngle + (div * 180);
    pointer.transition().duration(2500)
            .ease('elastic')
            .attr('transform', 'rotate(' + newAngle + ')');
}