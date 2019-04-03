

// https://bl.ocks.org/mbostock/4699541
// --> good example of transitions from country to another country (with click)


/**
 * TODO:
 * - Add select with all Regions. Ability to translate from a region to another. See https://bl.ocks.org/mbostock/4699541
 * 
 * - Better position tooltip (aligned below the mouse)
 * -  

 */
var width = 700, height = 550;

if (window.innerWidth >= 1000 && window.innerHeight >= 550) {
    width = 700;
    height = 550;

}
else {
   width = window.innerWidth - 30;
   height = window.innerHeight - 20;
}

console.log(width, height);

var active = d3.select(null);
var isZoomed = false;

const projection = d3.geoConicConformal() // Lambert-93
    .center([2.454071, 46.279229]) // Center on France
    // .center([2.44, 46.279229]) // Center on France
    .scale(2600)   //(2600)
    .translate([width / 2 - 50, height / 2]);

const path = d3.geoPath().projection(projection);

const svg = d3.select('#map').append("svg")
    .attr("id", "svg")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "Blues");

// Div used for tooltip
var div = d3.select("body").append("div")   
    .attr("class", "tooltip")               
    .style("opacity", 0);

// svg.append("rect")
//     .attr("class", "mybackground")
//     .attr("width", width)
//     .attr("height", height)
//     .on("click", reset);

// var g = svg.append("g")
//     .style("stroke-width", "1.5px")
//     .style("stroke", "black");

var g = svg.append("g")
    .style("stroke-width", "1px");
var regions = g.append('g')
    .style("stroke", "black");
const schoolsG = g.append('g');


var promises = [];
promises.push(d3.json('assets/regions.json'));
promises.push(d3.csv("assets/schools.csv")); // "assets/clean_school_positions.csv"
promises.push(d3.csv("assets/regions_with_closed_share.csv"));

Promise.all(promises).then(function(values) {
    const geojson = values[0]; // Récupération de la première promesse : le contenu du fichier JSON
    const schools = values[1]; // Récupération de la deuxième promesse : le contenu du fichier csv
    const regionData = values[2]; // Récupération de la deuxième promesse : le contenu du fichier csv
    
    // drawing the regions
    var features = regions
        .selectAll("path")
        .data(geojson.features)
        .enter()
        .append("path")
            .attr('id', function(d) {return "d" + d.properties.code;})
            // .attr("class", function(d) { return "department q1-9"; })
            .attr("d", path)
            .on("click", clicked);
    

    // Drawing the schools
    schools.forEach(d => {
        d.lat = +d.lat;
        d.lon = +d.lon;
        d.radius = 10;
    });
    const point = {
        type: 'Point',
        coordinates: [0, 0]
    };
    schools.forEach(d => {
        point.coordinates[0] = d.lon;
        point.coordinates[1] = d.lat;
        d.projected = path(point) ? projection(point.coordinates) : null;
    });

    const k = Math.sqrt(projection.scale() / 200);
    // const circles = schoolsG.selectAll('circle')
    //   .data(schools.filter(d => d.projected));

    const circles = schoolsG.selectAll('circle')
      .data(schools.filter(d => d.projected));

    circles.enter().append('circle')
      .merge(circles)
        .attr('cx', d => d.projected[0])
        .attr('cy', d => d.projected[1])
        .attr('fill', '#e43034')
        .attr('fill-opacity', 0.4)
        .attr('r', d => 1)
        .on('mouseover', function(d){
            if (isZoomed){
                console.log('zoomed tooltip')
                div.transition()        
                    .duration(300)      
                    .style("opacity", .9);
                div.html("<b>" + d.town + "</b> (" + Math.floor(+d.pop_count) + " habitants)<br>"
                        + "L'" + d.name + " a fermé en " + d.closed + ".<br>")
                    .style("left", (d3.event.pageX + 30) + "px")
                    .style("top", (d3.event.pageY - 30) + "px");

            }
        })
        .on('mouseout', function(d){
            div.style("opacity", 0);
        });
        // .attr('r', d => d.radius * k);
    circles.exit().remove();


    // Adding a color scale
    var quantile = d3.scaleQuantile()
        .domain([0, d3.max(regionData, function(e) { return +e.closed_share; })])
        .range(d3.range(9)); // we can change the number of colors here
    var title_legend = svg.append('text').attr('transform', 'translate(525, 110)');
   title_legend.text("Pourcentage d'écoles fermées").attr("font-size", 12);
    var legend = svg.append('g')
        .attr('transform', 'translate(525, 150)')
        .attr('id', 'legend')
        .attr('width', '20px')
        .attr('height', '20px');

    legend.selectAll('.colorbar')
        .data(d3.range(9))
        .enter().append('svg:rect')
            .attr('y', function(d) { return d * 20 + 'px'; })
            .attr('height', '20px')
            .attr('width', '20px')
            .attr('x', '0px')
            .attr("class", function(d) { return "q" + d + "-9"; });

    var legendScale = d3.scaleLinear()
        .domain([0, d3.max(regionData, function(e) { 
            console.log(e.closed_share)
            let text = String(+e.closed_share * 100);
            return text; })])
        .range([0, 9 * 20]);

    var legendAxis = svg.append("g")
        .attr('transform', 'translate(550, 150)')
        .call(d3.axisRight(legendScale).ticks(6));
        


    regionData.forEach(function(e,i) {
        console.log("#d" + e.region_code);

        d3.select("#d" + e.region_code)
            .attr("class", function(d) { return "department q" + quantile(+e.closed_share) + "-9"; })
            .on("mouseover", function(d) {
                if (!isZoomed){
                    div.transition()
                        .duration(300)
                        .style("opacity", .9);
                    div.html("<b>Région : </b>" + e.name + "<br>"
                            + "<b>Nombre d'écoles fermées entre la rentrée 2015 et la rentrée 2017 : </b>" + e.count + "<br>")
                        .style("left", (d3.event.pageX + 30) + "px")
                        .style("top", (d3.event.pageY - 30) + "px");
                }
            })
            .on("mouseout", function(d) {
                // d3.select(this).attr("stroke-width", 1);
                div.style("opacity", 0);
                // div.html("")
                //     .style("left", "-500px")
                //     .style("top", "-500px");
            });
    });

    // csv.forEach(function(e, i){

    //     var schools = g
    //         .selectAll('circle')
            

    //     e.lat, e.lon

    //     d3.select("#d" + e.CODE_DEPT)
    //         // .attr("class", function(d) { return "department q" + quantile(+e.POP) + "-9"; })
    //         .attr("class", function(d) { return "department q1-9"; })
    //         .on("mouseover", function(d) {
    //             div.transition()        
    //                 .duration(300)      
    //                 .style("opacity", .9);
    //             div.html("<b>Région : </b>" + e.NOM_REGION + "<br>"
    //                     + "<b>Département : </b>" + e.NOM_DEPT + "<br>"
    //                     + "<b>Population : </b>" + e.POP + "<br>")
    //                 .style("left", (d3.event.pageX + 30) + "px")     
    //                 .style("top", (d3.event.pageY - 30) + "px");
    //         })
    //         .on("mouseout", function(d) {
    //             // d3.select(this).attr("stroke-width", 1);
    //             div.style("opacity", 0);
    //             // div.html("")
    //             //     .style("left", "-500px")
    //             //     .style("top", "-500px");
    //         });
    // });

    // d3.select("select").on("change", function() {
    //     d3.selectAll("svg").attr("class", this.value);
    // });

    // d3.select("#data").on("change", function() {
    //     selectedData = this.value;
            
    //     quantile = d3.scale.scaleQuantile
    //         .domain([0, d3.max(csv, function(e) { return +e[selectedData]; })])
    //         .range(d3.range(9));
            
    //     legendScale.domain([0, d3.max(csv, function(e) { return +e[selectedData]; })]);
    //     legendAxis.call(d3.axisRight(legendScale).ticks(6));
            
    //     csv.forEach(function(e,i) {
    //         d3.select("#d" + e.CODE_DEPT)
    //             .attr("class", function(d) { return "department q" + quantile(+e[selectedData]) + "-9"; });
    //     });
    // });
    
});


function clicked(d) {
    // remove tooltip
    div.style("opacity", 0);

    if (active.node() === this) return reset();

    isZoomed = true;

    active.classed("active", false);
    active = d3.select(this).classed("active", true);
  
    var bounds = path.bounds(d),
        dx = bounds[1][0] - bounds[0][0],
        dy = bounds[1][1] - bounds[0][1],
        x = (bounds[0][0] + bounds[1][0]) / 2,
        y = (bounds[0][1] + bounds[1][1]) / 2,
        scale = .9 / Math.max(dx / width, dy / height),
        translate = [width / 2 - scale * x, height / 2 - scale * y];
  
    g.transition()
        .duration(750)
        .style("stroke-width", 1.5 / scale + "px")
        .attr("transform", "translate(" + translate + ")scale(" + scale + ")");
}

function reset() {
    isZoomed = false;

    active.classed("active", false);
    active = d3.select(null);

    g.transition()
        .duration(750)
        .style("stroke-width", "1.5px")
        .attr("transform", "");
}
