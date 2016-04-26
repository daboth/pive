
























//Created with pive 0.3.3 - the python interactive visualization environment.
//Visit https://github.com/daboth/pive for more information.

var width = 900;
var height = 600;
var padding	= 60;
var labelsize = 16;
var datakeys = ['1', '2'];
var url = 'piechart_sample.json';
var colors = ['#FF2C00', '#00B945', '#BF4930', '#238B49', '#A61D00', '#00782D', '#FF6140', '#37DC74', '#FF8B73', '#63DC90'];
var highlightopacity = 0.5;
var div_hook = 'chart';

var hashtag = '#';
var hash_div_hook = hashtag.concat(div_hook);








var root_div = document.getElementById(div_hook);


var css_line = '#chart .line { stroke: ; fill: none; stroke-width: 2.5px}\n',
    css_tooltip = '#chart .tooltip {color: white; line-height: 1; padding: 12px; font-weight: italic; font-family: arial; border-radius: 5px;}\n';
    css_axis_path = '#chart .axis path { fill: none; stroke: ; shape-rendering: crispEdges;}\n',
    css_axis_line = '#chart .axis line { stroke: ; shape-rendering: ;}\n',
    css_path_area = '#chart .path area { fill: blue; }\n';
    css_axis_text = '#chart .axis text {font-family: sans-serif; font-size: px }\n',
    css_xlabel_text = '#chart .xlabel {font-family: helvetica; font-size: px }\n',
    css_ylabel_text = '#chart .ylabel {font-family: helvetica; font-size: px }\n',
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

	var radius;
	if (width < height){
		radius = (width - padding) / 2;
	} else {
		radius = (height - padding) / 2;
	}

	var total = d3.sum(dataset, function(d){
		return d.value;
	});

	var percentformat = d3.format("0.1%");

	var tooltip = d3.select(hashtag.concat(div_hook)).append("div")
		    .attr("class", "tooltip")
		    .style("opacity", "0.0")
		    .style("position", "absolute")
		    .style("top", 0 + "px");




	var svg = d3.select(hashtag.concat(div_hook)).append("svg")
				.datum(dataset)
				.attr("width", width)
				.attr("height", height);

    var arc = d3.svg.arc().outerRadius(radius);
    var pie = d3.layout.pie().value(function(d) {
    	return d.value;
    });

    var arcs = svg.selectAll("g.arc")
    			  .data(pie)
    			  .enter()
    			  .append("g")
    			  .attr("class", "arc")
    			  .attr("transform", "translate(" + (radius + padding) + ", " + (radius + padding) + ")");

    arcs.append("path")
        .attr("fill", function(d, i){
        	return getColorIndex(i);
        })
        .attr("d", arc)
        .on("mouseover", function(d, i){
        	var tx = d3.mouse(this)[0];
        	var ty = d3.mouse(this)[1];
        	d3.select(this).transition()
        		           .attr("opacity", highlightopacity);
        	showTooltip([d.value, dataset[i].label], [tx, ty], i);
        })
        .on("mouseout", function(){
		    	hideTooltip();
		    	d3.select(this).transition()
        		           .attr("opacity", 1.0);
		    });



	function getColorIndex(index){
			var colorindex = index;
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

	    	tooltip.html((values[1] + ": " + values[0] + "<br><br><center>" + percentformat(values[0] / total)))
	    		   .style("left", ((position[0] + radius) +  "px"))
	    		   .transition()
	    		   .delay(600)
	    		   .duration(400)
	    		   .style("opacity", 1.0)
	    		   .style("position", "absolute")
	    		   .style("background-color", getColorIndex(accessor))
	    		   .style("top", ((position[1] + radius) + "px"));

	    }

});
