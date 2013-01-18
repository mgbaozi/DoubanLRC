(function ($) {
	
	function resize() {
		var bgImg = $('img#background');
		var wrap = $('div#wrap');
		
		var scale = Math.max($(window).height() / bgImg.height(), $(window).width() / bgImg.width());
		var newHeight = bgImg.height() * scale;
		var newWidth = bgImg.width() * scale;
		var newOffset = {
			top: ($(window).height() - newHeight) / 2,
			left: ($(window).width() - newWidth) / 2
		};
		bgImg.height(newHeight);
		bgImg.width(newWidth);
		bgImg.offset(newOffset);
		wrap.height($(window).height());
		wrap.width($(window).width());
		wrap.css('line-height', ($(window).height() * 0.95) + 'px');
		
		$('div#inner-background').css({
			'background-image': 'url("' + bgImg.attr('src') + '")',
			'background-position-x': (newOffset.left - $('div#inner-background').offset().left - parseInt($('div#inner-background').css('border-top-width'))) + 'px',
			'background-position-y': (newOffset.top - $('div#inner-background').offset().top - parseInt($('div#inner-background').css('border-top-width'))) + 'px',
			'background-position': (newOffset.left - $('div#inner-background').offset().left - parseInt($('div#inner-background').css('border-top-width'))) + 'px '
									+ (newOffset.top - $('div#inner-background').offset().top - parseInt($('div#inner-background').css('border-top-width'))) + 'px',
			'background-size': newWidth + 'px ' + newHeight + 'px'
		});
		if($.browser.msie && $.browser.version == '8.0') { $('div#inner-background').css('background','trasparent');}
	}
	
	$(document).ready(function () {
		
		$('div#wrap').css({
			'min-height': $('div#inner-wrap').height() + 'px',
			'min-width': $('div#inner-wrap').width() + 'px'
		});
		$('div#wrap').hide();
		
		$(window).resize(resize);
		window.onload = function () {
			$('div#wrap').show();
			resize();
		};
	});
})(jQuery);