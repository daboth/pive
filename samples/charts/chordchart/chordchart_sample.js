
























//Created with pive 0.3.3 - the python interactive visualization environment.
//Visit https://github.com/daboth/pive for more information.

var width = 900;
var height = 600;	
var padding	= 60;
var textpadding = 45;
var elementFontSize = '1.25em';
var	tickFontSize = '.75em"';
var	tickSteps = 1000;
var	prefix = 'K';
var url = 'chordchart_sample.json';
var div_hook = 'chart';

var hashtag = '#';
var hash_div_hook = hashtag.concat(div_hook);








var root_div = document.getElementById(div_hook);


var css_line = '#chart .line { stroke: black; fill: none; stroke-width: 2.5px}\n',
    css_tooltip = '#chart .tooltip {color: white; line-height: 1; padding: 12px; font-weight: italic; font-family: arial; border-radius: 5px;}\n';
    css_axis_path = '#chart .axis path { fill: none; stroke: black; shape-rendering: crispEdges;}\n',
    css_axis_line = '#chart .axis line { stroke: black; shape-rendering: optimizeSpeed;}\n',
    css_path_area = '#chart .path area { fill: blue; }\n';
    css_axis_text = '#chart .axis text {font-family: sans-serif; font-size: 16px }\n',
    css_xlabel_text = '#chart .xlabel {font-family: helvetica; font-size: 18px }\n',
    css_ylabel_text = '#chart .ylabel {font-family: helvetica; font-size: 18px }\n',
    css_x_axis_line = '#chart .x.axis line { stroke: grey; stroke-opacity: 0.25; stroke-width: 2.5px}\n',
    css_y_axis_line = '#chart .y.axis line { stroke: grey; stroke-opacity: 0.25; stroke-width: 2.5px}';


var css = css_line.concat(css_tooltip).concat(css_axis_path).concat(css_axis_line).concat(css_path_area).concat(css_axis_text)
          .concat(css_xlabel_text).concat(css_ylabel_text).concat(css_x_axis_line).concat(css_y_axis_line);


var style = document.createElement('style');
style.type = 'text/css';
style.appendChild(document.createTextNode(css));
root_div.appendChild(style);





var innerRadius = Math.min(width, height) * .34,
	outerRadius = innerRadius * 1.2,
	labelFont = "Helvetica",
	transistionSpeed = 500;




var svg = d3.select(hashtag.concat(div_hook)).append("svg")
			.attr("width", width)
			.attr("height", height)
			.append("g")
			.attr("transform", "translate(" + width/2 + "," + height/2 + ")");

var fill = ['#FF2C00', '#00B945', '#BF4930', '#238B49', '#A61D00', '#00782D', '#FF6140', '#37DC74', '#FF8B73', '#63DC90'];

d3.json(url, function(data){

	console.log(data.elements);
	var chordElements = data.elements;
	var matrix = data.matrix;
	console.log(matrix)

	function getColorIndex(index){
			var colorindex = index;
		   	var color;

		   	while (colorindex > fill.length - 1) {
		   		colorindex = colorindex - fill.length;

		   	}
		   	
		   	color = fill[colorindex];
		   	return color;
		}  	

	function generateChord() {		

		svg.selectAll("rect").remove();
		svg.selectAll("g").remove();

		svg.attr("transform", "translate(" + width/2 + "," + height/2 + ")");


		var chord = d3.layout.chord()
				.matrix(matrix)
				.padding(0.05)
				.sortSubgroups(d3.descending);		

		//Select all groups from class "chordGroup"
		var chordGroup = svg.selectAll("g.chordGroup")
					.data(chord.groups)
					.enter().append("svg:g")
					.attr("class", "chordGroup");

		var arc = d3.svg.arc()
					.innerRadius(innerRadius)
					.outerRadius(outerRadius);

		chordGroup.append("path")
			.attr("d", arc)
			.style("fill", function(d) {						
				return getColorIndex(d.index);
			})
			.style("stroke", function(d) {
				return getColorIndex(d.index);
			})
			.attr("id", function(d, i) {
				return "group-" + d.index;
			});

		chordGroup.append("text")
		      .each(function(d) { d.angle = (d.startAngle + d.endAngle) / 2; })
		      .attr("dy", ".35em")
		      .attr("font-size", elementFontSize)
		      .attr("font-family", labelFont)
		      .attr("transform", function(d) {
		        return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
		            + "translate(" + (outerRadius + textpadding) + ")"
		            + (d.angle > Math.PI ? "rotate(180)" : "");
		      })
		      .style("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
		      .text(function(d) { return chordElements[d.index]; });



		//Eventlistener for each chordGroup group.
	    chordGroup.on("mouseover", fade(0.05))
			      .on("mouseout", fade(0.75))
			      .on("click", function(d,i) {
			      	showDetail(i);
			      });


	     svg.append("g")
	        .attr("class", "chord")
	        .selectAll("path")
	        .data(chord.chords)
	        .enter().append("path")
	        .attr("d", d3.svg.chord().radius(innerRadius))
	        .style("fill", function(d) {
	        	return chordColor(d);
	        })	
	        .style("stroke", function(d) {
	        	return chordColor(d);
	        })			        
	        .style("opacity", 0.75); 

		var ticks = svg.append("g").selectAll("g")
				   .data(chord.groups)
				   .enter().append("g").selectAll("g")
				   .data(chordTicks)
				   .enter().append("g")
				   .attr("class", "ticks")
				   .attr("transform", function(d) {
				      return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
				          + "translate(" + outerRadius + ",0)";
				    });
				   

		ticks.append("line")
		    .attr("x1", 1)
		    .attr("y1", 0)
		    .attr("x2", 5)
		    .attr("y2", 0)
		    .style("stroke", "#111");

		ticks.append("text")
		    .attr("x", 8)
		    .attr("dy", ".35em")
		    .attr("font-size", tickFontSize)
		    .attr("font-family", labelFont)
		    .attr("transform", function(d) { return d.angle > Math.PI ? "rotate(180)translate(-16)" : null; })
		    .style("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
		    .text(function(d) { return d.label; });

	}

	function chordColor(d) {

				var colorindex = (d.source.value > d.target.value ?
	            d.source.index : d.target.index);
	        return getColorIndex(colorindex);
	    }
	     

	function fade(opacity) {
	    return function(d, i) {
	        svg.selectAll(".chord path")
	            .filter(function(d) {		                	
	                return d.source.index != i &&
	                       d.target.index != i;
	            })
	            .transition()
	            .duration(transistionSpeed)
	            .style("opacity", opacity);
	    };
	};

	//Draws a detailed BarChart containing the absolute weight of the graphnode.
	function showDetail(index) {

		svg.attr("transform", "translate(0,0)");

			svg.selectAll("g").remove()

			detailwidth = width / 1.5;
			detailheight = height / 2;

			var color = getColorIndex(index);
		
			var dataset = matrix[index];

			console.log(dataset);

			var xScale = d3.scale.ordinal()
					.domain(d3.range(dataset.length))
					.rangeRoundBands([0, detailwidth - padding], 0.1);

		var yScale = d3.scale.linear()
					.domain([1, d3.max(dataset)])
					.range([0, detailheight - padding]);

		var xAxisScale = d3.scale.ordinal()
					.domain(chordElements)
					.rangeRoundBands([0, detailwidth - padding], 0.1);

		var yAxisScale = d3.scale.linear()
				.domain([1, d3.max(dataset)])
				.range([detailheight - padding, 0]);


		//Define X axis
		var xAxis = d3.svg.axis()
					  .scale(xAxisScale)
					  .orient("bottom")
					  .ticks(5);

		//Define Y axis
		var yAxis = d3.svg.axis()
					  .scale(yAxisScale)
					  .orient("left")
					  .ticks(10);

	    //Create X axis
		svg.append("g")
			.attr("opacity", 0.0)
			.attr("class", "x axis")
			// .attr("transform", "translate(0," + (detailheight - padding) + ")")
			.attr("transform", "translate("+ padding + "," + (detailheight - padding) + ")")
			.call(xAxis)
			.transition()
			.duration(transistionSpeed)
			.attr("opacity", 1.0);

		//Create Y axis
		svg.append("g")					
			.attr("opacity", 0.0)
			.attr("class", "y axis")
			.attr("transform", "translate(" + padding + ",0)")
			.call(yAxis)
			.transition()
			.duration(transistionSpeed)
			.attr("opacity", 1.0);

		var bars = svg.selectAll("rect")
	       .data(dataset)
	       .enter()
	       .append("rect")
	       .attr("opacity", 0.0)
	       .attr("fill", color)			      
		   .on("click", generateChord)
	       .transition()
	       .duration(transistionSpeed)
	       .attr("class", "bar")
	       .attr("opacity", 1.0)
	       .attr("x", function (d, i) {
	       		return xScale(i) + padding;
	       })
	       .attr("y", function (d) {
	       		return detailheight - yScale(d) - padding; 
	       })
	       .attr("width", xScale.rangeBand())
	       .attr("height", function (d){
	       		return yScale(d);
	       });		        
	};
	 
	 
	// Returns tick angles.
	function chordTicks(d) {
	  var k = (d.endAngle - d.startAngle) / d.value;

	  return d3.range(0, d.value, tickSteps).map(function(v, i) {
	    return {
	      angle: v * k + d.startAngle,
	      label: i % 5 ? null : v / tickSteps + prefix
	    };
	  });
	};
	generateChord();
});	