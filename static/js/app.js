var jobsApp = (function(){
	'use strict';

	var DEBUG = false;
	var $loader = $('.loader');
	var $results = $('#results');

	function loadJSON(e) {
		var filename = $(this).attr('href') + '.json';
		loader('Loading');
		e.preventDefault();
		e.stopImmediatePropagation();
		d3.json(filename, function(data) {
			// SEE: https://github.com/mbostock/d3/wiki/Requests
			if(!data) {
				$results.html('File does not exist or could not be loaded.');
				unloader();
				return;
			}
			loader('Adding...');
			$results.empty();
			loaded(data);
		});
	}

	function loader(msg) {
		$loader.removeClass('hidden');
		$results.removeClass('hidden');
		if(!msg) return;
		$loader.find('.content').text(msg);
	}

	function unloader() {
		$loader.addClass('hidden');
	}

	function loaded(data) {
		if(DEBUG) log(data);
		// TODO: visualizations
		var $svg = d3.select('#results');
		var text = $svg.append('g').attr('class', 'text-group');

		text.selectAll('p')
		.data(data)
		.enter()
		.append('p')
		.html(function(d){
			return '<div class="well">' + (d.job_ID ? 'JOB #' + d.job_ID : 'No ID.') + ' <a href="' + d.url + '">View job</a>' + '<br /><small>' + (d.description ? d.description : 'No description.') + '</small></div>';
		});
		unloader();
	}

	function log(data) {
		if(console && typeof console === 'object') {
			console.log(data);
		}
	}

	function init(data) {
		var $links = $('.json-file');
		$links.on('click', loadJSON);
	}

	return {
		'init': init
	};

})();

$(document).ready(jobsApp.init);
