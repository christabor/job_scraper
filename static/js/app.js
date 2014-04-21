var jobsApp = (function(){
	'use strict';

	var $loader = $('.loader');
	var $results = $('#results');

	function loadData(e) {
		var filename = $(this).attr('href');
		loader();
		e.preventDefault();
		e.stopImmediatePropagation();
		d3.json(filename, function(error, json) {
			// SEE:
			// https://github.com/mbostock/d3/wiki/Requests
			if(error) {
				$results.html('Could not load this file.')
				unloader();
				return;
			}
			loaded($.parseJSON(json));
		});
	}

	function loader() {
		$loader.removeClass('hidden');
		$results.removeClass('hidden');
	}

	function unloader() {
		$loader.addClass('hidden');
	}

	function loaded(data) {
		log(data);
		var w = $results.width();
		var $svg;
		$results.empty();
		$svg = d3.select('#results')
		.append('svg')
		.attr('width', w)
		.attr('height', w);

		var text = $svg.append('g')
		.attr('id', 'text-group');
		text.selectAll('text')
		.data(data)
		.enter()
		.append('text')
		.attr('x', function(k, d){
			return 0;
		})
		.attr('y', function(k, d){
			return d * 20 + 20;
		})
		.text(function(d){
			log(d);
			return d.education;
		});

		$svg.selectAll('rect').data(data)
		.enter()
		.append('rect')
		.attr('height', function(k, d){
			log(k);
			log(d);
		})
		.attr('width', function(k, d){
			return k * 2;
		});
	}

	function log(msg) {
		console.log(msg);
	}

	function init(data) {
		var $links = $('.json-file');
		$links.on('click', loadData);
	}

	return {
		'init': init
	};

})();

$(document).ready(jobsApp.init);
