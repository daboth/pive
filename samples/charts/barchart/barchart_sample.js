
























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
var datakeys = ['1', '2'];
var timeformat = '';
var iconwidth = 20;
var iconheight = 40;
var iconcolor = '#FF2C00';
var iconhighlight = '#FF8B73';
var verticalscale = 'linear';
var barbreak = 0.2;
var div_hook = 'chart';

var url = 'barchart_sample.json';
var threshold = '1';
var filter;

if ((width / viewport) < threshold){
	filter = parseInt(threshold * (viewport / width));
};


var colors = ['#FF2C00', '#00B945', '#BF4930', '#238B49', '#A61D00', '#00782D', '#FF6140', '#37DC74', '#FF8B73', '#63DC90'];
var tickrotation = -45;

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
  
    var vertical_extent = d3.extent(dataset, function(d){ return d.value});
    
    var yScale;
    var yAxisScale;

	var barScale = d3.scale.ordinal()
        .domain(d3.range(viewdata.length))
        .rangeRoundBands([padding + iconwidth + labelsize, width - padding - iconwidth], barbreak);

    barScale.domain(viewdata.map(function(d){
    	return d.label;
    }));

    scaleYAxis();

    function scaleYAxis(){			    	
    	//###################################
    	//######## scale the x-axis. ########
    	//###################################
    	if (verticalscale == 'linear') {
    		//Provide a linear scaling.
    		yScale = d3.scale.linear()
    			   .range([padding + labelsize, height - ((2 * padding) + labelsize)])
    			   .domain(vertical_extent);
		    yAxisScale = d3.scale.linear()
    			   .range([height - padding, padding + labelsize])
    			   .domain(vertical_extent);

    	} else if (verticalscale == 'log') {
    		if (vertical_extent[0] <= 0){
    			yScale = d3.scale.linear()
    			   .range([padding + labelsize, height - ((2 * padding) + labelsize)])
    			   .domain(vertical_extent);
		    	yAxisScale = d3.scale.linear()
    			   .range([height - padding, padding + labelsize])
    			   .domain(vertical_extent);
    		
    		} else {
    			yScale = d3.scale.log()
        			   .range([padding + labelsize, height - padding])         			   
        			   .domain(vertical_extent);
		    	yAxisScale = d3.scale.log()
        			   .range([height - padding, padding + labelsize])         			   
        			   .domain(vertical_extent);
    		}

    		
    	} else if (verticalscale.substring(0,3) == 'pow') {	
    		
    		//The exponent of the power scale is indicated by a number
    		//following the 'pow', e.g. 'pow2'.
    		exp = parseInt(scales[1].substring(3, scales[1].length));
    		
    		//Provide a power scaling.
    		yScale = d3.scale.pow()
    				   .exponent(exp)
        			   .range([padding + labelsize, height - padding])		   
        			   .domain(vertical_extent);
		    yAxisScale = d3.scale.pow()
    				   .exponent(exp)
        			   .range([height - padding, padding + labelsize])		   
        			   .domain(vertical_extent);
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
		xaxis.orient('bottom')
			 .tickValues(barScale.domain().filter(function(d, i) { return !(i % filter); }))
		     .scale(barScale);

	};

	function initializeYAxis() {
		yaxis.orient('left')	    			
    		 .scale(yAxisScale); 
	};

    initializeXAxis();		
    initializeYAxis();	

    function barUpdate() {
    	var bars = svg.selectAll("rect").data(viewdata);

        bars.enter()
	        .append("rect")
	        .attr("opacity", 0.0);	    

        bars.exit().remove();

        bars.attr("class", "bar")
        	.transition()
        	.duration(750)
        	.ease("elastic")
        	.attr("opacity", 1.0)
	        .attr("x", function (d) {
	        	return barScale(d.label);
		    })
		        .attr("y", function (d) {
		        return (height - padding - labelsize) - yScale(d.value);
		    })
		        .attr("height", function (d) {
		        return yScale(d.value);
		    })
		        .attr("width", function (d) {
		        return barScale.rangeBand();
		    })
		        .attr("fill", function (d, i) {
		        return getColorIndex(i);
		    });

        bars.on("mouseover", function(d, i){
	        	var tx = d3.mouse(this)[0];
	        	var ty = d3.mouse(this)[1];
	        	d3.select(this).transition()
	        		           .attr("opacity", 0.5);
	            console.log(viewdata[i].label);
	        	showTooltip([d.value, viewdata[i].label], [tx, ty], i);
	        })
        	.on("mouseout", function(){
		    	hideTooltip();
		    	d3.select(this).transition()
        		           .attr("opacity", 1.0);
		    });	 

        
    }

    barUpdate();

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
	
	function forwardData() {
		current_offset += jumplength;
		
		if ((current_offset + viewport) > dataset.length) {
			viewdata = dataset.slice(current_offset, dataset.length);
			current_offset -= jumplength;
		} else {
			viewdata = dataset.slice(current_offset, current_offset + viewport);
		};
		
	    barScale.domain(viewdata.map(function(d){
	    	return d.label;
	    }));	  

	    updateAxes();	
	    barUpdate();

	};

	
	function backwardData() {
		current_offset -= jumplength;
		
		if (current_offset < 0) {
			viewdata = dataset.slice(0, 0 + viewport);
			current_offset = 0;
		} else {
			viewdata = dataset.slice(current_offset, current_offset + viewport);
		};
		
	    barScale.domain(viewdata.map(function(d){
	    	return d.label;
	    }));	  

	    updateAxes();
	    barUpdate();		
	};
	
	
	function updateAxes(){

		xaxis.tickValues(barScale.domain().filter(function(d, i) { return !(i % filter); }));

		svg.select(".x.axis")
    		.transition()    		
    		.duration(250)
    		.call(xaxis)

		svg.select(".y.axis")
    		.transition()    		
    		.duration(250)
    		.call(yaxis)
    		
		svg.select(".x.axis")
			.selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", function(d) {
                return "rotate(" + tickrotation + ")" 
            });

	};


	function getColorIndex(y_accessor){
			var colorindex = y_accessor;
		   	var color;

		   	while (colorindex > colors.length - 1) {
		   		colorindex = colorindex - colors.length;

		   	}
		   	
		   	color = colors[colorindex];
		   	return color;
		}  	
    

   function hideTooltip(){
    	tooltip.transition()
    	.duration(200)
    	.style("opacity", 0.0)
    	.style("top", 0 + "px");
    }

    function showTooltip(values, position, accessor){
	    	//console.log("tooltip")
	    	var keyindex = parseInt(accessor) + 1;
	    	
	    	tooltip.text(values[1] + ": " + values[0])
	    		   .style("left", (position[0] + "px"))
	    		   .transition()
	    		   .delay(600)
	    		   .duration(400)
	    		   .style("opacity", 1.0)
	    		   .style("position", "absolute")	    		   
	    		   .style("background-color", getColorIndex(accessor))
	    		   .style("top", (position[1] + "px"));

	    }

});