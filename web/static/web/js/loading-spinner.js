$(document).ready(function($) {
	(function() {
		var galeria = $('.img')
        if (window.innerWidth > 768) {
            var alturaLoading = galeria.height() - 700;
            var anchoLoading = galeria.width() - 700;
        } else {
            var alturaLoading = galeria.height() - 300;
            var anchoLoading = galeria.width() - 250;
        }
		$('.loader').css({top: alturaLoading, right:anchoLoading, position: 'absolute'})
	})()
});

$(window).load(function() {
	//$('.loader').hide('slow');
	$('.loader').show();
});