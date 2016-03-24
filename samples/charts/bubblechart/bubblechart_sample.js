
























//Created with pive 0.3.3 - the python interactive visualization environment.
//Visit https://github.com/daboth/pive for more information.

var width = 900;
var height = 600;
var padding	= 60;
var labelsize = 18;
var viewport = 50;
var jumplength = 10;
var xlabel = 'X';
var ylabel = 'Y';
var datakeys = ['x', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6'];
var timeformat = '%H:%M:%S';
var iconwidth = 20;
var iconheight = 40;
var iconcolor = '#FF2C00';
var iconhighlight = '#FF8B73';
var url = 'bubblechart_sample.json';
var iso = d3.time.format.utc('%H:%M:%S');
var scales = ['linear', 'linear'];
var colors = ['#FF2C00', '#00B945', '#BF4930', '#238B49', '#A61D00', '#00782D', '#FF6140', '#37DC74', '#FF8B73', '#63DC90'];
var tickrotation = -45;
var circleopacity = 0.5;
var highlightfactor = 1.1;
var minradius = 1;
var maxradius = 50;
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





d3.json(url, function(data){
	//The complete dataset.
	var dataset = data;
	//The current offset starting at zero.
	var current_offset = 0;
	//Define the viewport of the data. Only a slice of the full dataset is currently shown.
    var viewdata = dataset.slice(current_offset, current_offset + viewport);

    //Determines the maximum y-value considering each datapoints maximum.
    var max_y = d3.max(data, function(d){
    	var datapoint_max = d.y[0][0];
    	for (var i = 0; i < d.y.length; i++)
    		if (d.y[i][0] > datapoint_max){
    			datapoint_max = d.y[i][0];
    		}
		return datapoint_max;
    });

    var max_radius = d3.max(data, function(d){
    	var datapoint_max = d.y[0][1];
    	for (var i = 1; i < d.y.length; i++)
    		if (d.y[i][1] > datapoint_max){
    			datapoint_max = d.y[i][1];
    		}
		return datapoint_max;
    });

    //Determines the minimum y-value considering each datapoints minimum.
    var min_y = d3.min(data, function(d){
    	var datapoint_min = d.y[0][0];
    	for (var i = 0; i < d.y.length; i++)
    		if (d.y[i][0] < datapoint_min){
    			datapoint_min = d.y[i][0];
    		}
		return datapoint_min;
    });

    //Determines the minimum y-value considering each datapoints minimum.
    var min_radius = d3.min(data, function(d){
    	var datapoint_min = d.y[0][1];
    	for (var i = 0; i < d.y.length; i++)
    		if (d.y[i][1] < datapoint_min){
    			datapoint_min = d.y[i][1];
    		}
		return datapoint_min;
    });

    //The extent of all datapoint values consists of their minima and maxima.
    var x_extent = d3.extent(viewdata, function(d){ return d.x});
    var y_extent = [min_y, max_y];
    var radius_extent = [min_radius, max_radius]
    var xScale;
    var yScale;
    var yAxisScale;
    var circleScale;

    scaleXAxis();
    scaleYAxis();
    scaleCircle(minradius, maxradius);

    function scaleCircle(minradius, maxradius){

    	var circlerange = [minradius, maxradius];
    	circleScale = d3.scale.linear()
    					.range(circlerange)
    					.domain(radius_extent);
    };


    //Creates a new date object of a given timestamp.
    function getDateFromTime(time){
    	try {
    		return new Date(time);
    	} catch (err) {
    		console.log("An Error occured while parsing the date object.");
    		console.log(err.message);
    		return null;
    	};

    };

    function scaleXAxis(){
    	//###################################
    	//######## scale the x-axis. ########
    	//###################################
    	var xrange = [padding + labelsize + iconwidth, width - padding];

    	if (scales[0] == 'linear') {
    		//Provide a linear scaling.
    		xScale = d3.scale.linear()
        			   .range(xrange)
        			   .domain(x_extent);

    	} else if (scales[0] == 'log') {
    		if (x_extent[0] <= 0){
    			xScale = d3.scale.linear()
        			   .range(xrange)
        			   .domain(x_extent);
    		} else {
    			xScale = d3.scale.log()
        			   .range(xrange)
        			   .domain(x_extent);
    		}


    	} else if (scales[0].substring(0,3) == 'pow') {

    		//The exponent of the power scale is indicated by a number
    		//following the 'pow', e.g. 'pow2'.
    		exp = parseInt(scales[0].substring(3, scales[0].length));

    		//Provide a power scaling.
    		xScale = d3.scale.pow()
    				   .exponent(exp)
        			   .range(xrange)
        			   .domain(x_extent);

	    } else if (scales[0] == 'date') {
	    	//Date-code to be implemented.
	    	var minDate = getDateFromTime(x_extent[0]);
	    	var maxDate = getDateFromTime(x_extent[1]);

	    	xScale = d3.time.scale()
	    			   .range(xrange)
	    			   .domain([minDate, maxDate]);
		};
    };

    function scaleYAxis(){
    	//###################################
    	//######## scale the x-axis. ########
    	//###################################
    	if (scales[1] == 'linear') {
    		//Provide a linear scaling.
    		yScale = d3.scale.linear()
    			   .range([padding + labelsize, height - padding])
    			   .domain(y_extent);
		    yAxisScale = d3.scale.linear()
    			   .range([height - padding, padding + labelsize])
    			   .domain(y_extent);

    	} else if (scales[1] == 'log') {

    		if (y_extent[0] <= 0){
    			yScale = d3.scale.linear()
    			   .range([padding + labelsize, height - padding])
    			   .domain(y_extent);
		    	yAxisScale = d3.scale.linear()
    			   .range([height - padding, padding + labelsize])
    			   .domain(y_extent);
    		} else {
    			yScale = d3.scale.log()
        			   .range([padding + labelsize, height - padding])
        			   .domain(y_extent);
		   		 yAxisScale = d3.scale.log()
        			   .range([height - padding, padding + labelsize])
        			   .domain(y_extent);
    		}


    	} else if (scales[1].substring(0,3) == 'pow') {

    		//The exponent of the power scale is indicated by a number
    		//following the 'pow', e.g. 'pow2'.
    		exp = parseInt(scales[1].substring(3, scales[1].length));

    		//Provide a power scaling.
    		yScale = d3.scale.pow()
    				   .exponent(exp)
        			   .range([padding + labelsize, height - padding])
        			   .domain(y_extent);
		    yAxisScale = d3.scale.pow()
    				   .exponent(exp)
        			   .range([height - padding, padding + labelsize])
        			   .domain(y_extent);

	    } else if (scales[1] == 'date') {
	    	//Date-code to be implemented.
	    	var minDate = getDateFromTime(y_extent[0]);
	    	var maxDate = getDateFromTime(y_extent[1]);
	    	yScale = d3.time.scale()
	    			   .range([padding + labelsize, height - padding])
	    			   .domain([minDate, maxDate]);
		    yAxisScale = d3.time.scale()
	    			   .range([height - padding, padding + labelsize])
	    			   .domain([minDate, maxDate]);
		};
    };




	var svg = d3.select(hashtag.concat(div_hook)).append("svg")
				.attr("width", width)
				.attr("height", height);

	var tooltip = d3.select(hashtag.concat(div_hook)).append("div")
			    .attr("class", "tooltip")
			    .style("opacity", "0.0")
			    .style("top", 0 + "px");

	var xaxis = d3.svg.axis();
	var yaxis = d3.svg.axis();

	//X Axis initialization.
	function initializeXAxis() {

		if (scales[0] == 'date') {
			xaxis.ticks(d3.time.milliseconds, 10)
    		     .tickFormat(d3.time.format(timeformat))
			     .tickSize(-(height - padding * 2 - labelsize), 0, 0)
    		     .scale(xScale);
		} else {

			xaxis.tickSize(-(height - padding * 2 - labelsize), 0, 0)
			     .scale(xScale);
		};
	};

	function initializeYAxis() {
		yaxis.orient('left')
    		 .scale(yAxisScale);

	};

    initializeXAxis();
    initializeYAxis();

	var xa = svg.append('g')
			   .attr('class', 'x axis')
			   .attr('transform', 'translate(0, ' + (height - padding - labelsize) + ')')
			   .data(viewdata)
			   .call(xaxis)
			   .selectAll("text")
	            .style("text-anchor", "end")
	            .attr("dx", "-.8em")
	            .attr("dy", ".15em")
	            .attr("transform", function(d) {
	                return "rotate(" + tickrotation + ")"
	                });

	var ya = svg.append('g')
			   .attr('class', 'y axis')
			   .attr('transform', 'translate('+ (padding + labelsize + iconwidth) + ', ' + (-labelsize) + ')')
			   .data(viewdata)
			   .call(yaxis);

    var bottom_label = svg.append("text")
    					  .attr("class", "x label")
    					  .attr("x", (width / 2) + (padding / 2))
    					  .attr("y", height)
    					  .style("text-anchor", "middle")
    					  .style("font-size", labelsize)
    					  .text(xlabel);

    var left_label = svg.append("text")
   						  .attr("class", "y label")
    					  .attr("transform", "rotate(-90)")
				  		  .attr("x", (- height / 2) + (padding / 2))
    					  .attr("y", 0)
    					  .attr("dy", "1em")
    					  .style("text-anchor", "middle")
    					  .style("font-size", labelsize)
    					  .text(ylabel);

	function drawButtons(){
		//Append the buttons.
	    var buttons = svg.append("g")
	    				 .attr("class", "button")

	    var vertical_center = (height / 2) - (padding / 2) - (iconheight / 2);

	   	//Prepare the transformation.
	    var right_translation = 'translate(' + (width - iconwidth) + ',' + (vertical_center) + ')';
	    var left_translation = 'translate(' + (iconwidth + 10 + labelsize) + ',' + (vertical_center) + ')';

		//Append the right arrow button and apply its transformation.
		buttons.append("path")
			.attr('d', 'm 0 0 0 ' + iconheight + ' ' + iconwidth + ' -' + iconheight / 2 + 'z')
	        .attr('transform', right_translation)
	        .attr('fill', iconcolor)
	        .on("click", function() {
			  		forwardData();
			})
			.on('mouseover', function() {
				d3.select(this).attr('fill', iconhighlight);
			})
			.on('mouseout', function() {
				d3.select(this).attr('fill', iconcolor);
			});

		//Append the left arrow button and apply its transformation.
		buttons.append("path")
			.attr('d', 'm 0 0 0 ' + iconheight + ' -' + iconwidth + ' -' + iconheight / 2 + 'z')
	        .attr('transform',  left_translation)
	        .attr('fill', iconcolor)
	        .on("click", function() {
			  		backwardData();
			})
			.on('mouseover', function() {
				d3.select(this).attr('fill', iconhighlight);
			})
			.on('mouseout', function() {
				d3.select(this).attr('fill', iconcolor);
			});

	}

	if (viewport > viewdata.length){
		viewport = viewdata.length;
	} else {
		drawButtons();
	}


	function updateXAxis(new_extent) {

		if (scales[0] == 'date') {
			var minDate = iso(getDateFromTime(new_extent[0]));
	    	var maxDate = iso(getDateFromTime(new_extent[1]));
			xScale.domain([minDate, maxDate]);
		} else {
			xScale.domain(new_extent);
		}

	}

	function forwardData() {
		current_offset += jumplength;

		if ((current_offset + viewport) > dataset.length) {
			viewdata = dataset.slice(current_offset, dataset.length);
			current_offset -= jumplength;
		} else {
			viewdata = dataset.slice(current_offset, current_offset + viewport);
		};


		x_extent = d3.extent(viewdata, function(d){ return d.x});


		if (scales[0] == 'date') {
			var minDate = getDateFromTime(x_extent[0]);
	    	var maxDate = getDateFromTime(x_extent[1]);
			xScale.domain([minDate, maxDate]);
		} else {
			xScale.domain(x_extent);
		};

		updateView();

	};


	function backwardData() {
		current_offset -= jumplength;

		if (current_offset < 0) {
			viewdata = dataset.slice(0, 0 + viewport);
			current_offset = 0;
		} else {
			viewdata = dataset.slice(current_offset, current_offset + viewport);
		};


		x_extent = d3.extent(viewdata, function(d){ return d.x});


		if (scales[0] == 'date') {
			var minDate = getDateFromTime(x_extent[0]);
	    	var maxDate = getDateFromTime(x_extent[1]);
			xScale.domain([minDate, maxDate]);
		} else {
			xScale.domain(x_extent);
		};

		updateView();

	};


	function updateView(){

		svg.select(".x.axis")
    		.transition()
    		.duration(250)
    		.call(xaxis)

		svg.select(".x.axis")
			.selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", function(d) {
                return "rotate(" + tickrotation + ")"
            });

        svg.selectAll(".circle").remove();

		for (var i = 0; i < viewdata[0].y.length; i++)
			drawData(i);

	};

	var circles = svg.selectAll("circle");


	for (var i = 0; i < viewdata[0].y.length; i++)
		drawData(i);

	function getColorIndex(y_accessor){
			var colorindex = y_accessor;
		   	var color;

		   	while (colorindex > colors.length - 1) {
		   		colorindex = colorindex - colors.length;

		   	}

		   	color = colors[colorindex];
		   	return color;
		}

    function drawData(y_accessor){
    	//If no y_accessor was defined, the data is assumed to contain only one dataset.
    	//the y_accessor then becomes obsolete.
    	y_accessor = (typeof y_accessor == "undefined") ? 1 : y_accessor;

	    function drawCircles(index){

	    	circles = svg.append("circle")
	    			 .datum(viewdata)
	    			 .attr("class", "circle")
	    			 .attr('fill', 'white')
	    			 .transition()
	    			 .duration(200)
	    			 .attr("cx", function(d) {
	    			 	return xScale(d[index].x);
	    			 })
	    			 .attr("cy", function(d) {
	    			 	return height - yScale(d[index].y[y_accessor][0]);
	    			 })
	    			 .attr("r", function(d){
	    			 	return circleScale(d[index].y[y_accessor][1]);
	    		 	 })
	    			 .attr("xvalue", function(d){
	    			 	return d[index].x;
	    			 })
	    			 .attr("yvalue", function(d){
	    			 	return d[index].y[y_accessor][0];
	    			 })
	    			 .attr("y_accessor", y_accessor)
	    			 .attr("opacity", circleopacity)
	    			 .attr("fill", getColorIndex(y_accessor));
	    }

		for (var i = 0; i < viewdata.length; i++)
			drawCircles(i);





	    svg.selectAll("circle")
	    	.on("mouseover", function(){
		    	var xvalue = d3.select(this).attr("xvalue");
		    	var yvalue = d3.select(this).attr("yvalue");
		    	var circlex = d3.select(this).attr("cx");
		    	var circley = d3.select(this).attr("cy");
		    	var accessor = d3.select(this).attr("y_accessor");


		    	var values = [xvalue, yvalue];
		    	var position = [circlex, circley];
		    	var coords = d3.mouse(this);

		    	d3.select(this).transition()
		    	.duration(500)
		    	.attr('opacity', (circleopacity / 2))
		    	.attr('r', d3.select(this).attr('r') * highlightfactor)
		    	.each('end', showTooltip(coords, values, position, accessor));
		    })
		    .on("mouseout", function(){
		    	d3.select(this).transition()
		    	.attr('opacity', circleopacity)
		    	.attr('r', d3.select(this).attr('r') / highlightfactor);
		    	hideTooltip();
		    });
    };

   function hideTooltip(){
    	tooltip.transition()
    	.duration(200)
    	.style("opacity", 0.0)
    	.style("top", 0 + "px");
    }

    function showTooltip(coords, values, position, accessor){
	    	var keyindex = parseInt(accessor) + 1;

	    	tooltip.text(datakeys[0] + ": " + values[0] + " " + datakeys[keyindex] + ": " + values[1])
	    		   .style("left", (position[0] + "px"))
	    		   .transition()
	    		   .delay(600)
	    		   .duration(400)
	    		   .style("opacity", 1.0)
	    		   .style("position", "absolute")
	    		   .style("background-color", getColorIndex(accessor))
	    		   .style("top", ((position[1] - (maxradius)) + "px"));

	    }

});
