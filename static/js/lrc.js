(function ($) {
	
	var maxLrcOnDisplay = 17;
	var refreshInterval = 50;
	var timeOffsetPerScroll = 400;
	
	var slideBox = { };
	var lrcItems = { };
	var activeLrcItems = { };
	
	var songInfo = { };
	var lrcList = [];
	var startTime = new Date().getTime();
	var currentPos = 0;
	var lrcState = 0;
	
	function textOpacityEasing(offset) {
		return Math.sqrt(Math.abs(Math.cos(offset * Math.PI / 2)));
	}
	
	function getPosByTime(time) {
		var pos = 0;
		var nextPos = 1;
		for(var index in lrcList) {
			if(time >= lrcList[index].time) {
				pos = parseInt(index);
			} else {
				if(index == 0) return 3 * (time / lrcList[0].time - 1);
				break;
			}
		}
		var posOffset = (1 - Math.cos((time - lrcList[pos].time) * Math.PI / (lrcList[pos + 1].time - lrcList[pos].time))) / 2;
		return pos + posOffset;
	}
	
	function initAttribute() {
		for(var index in lrcList) {
			slideBox.append('<p class="lrc">&zwnj;' + lrcList[index].lrc + '</p>');
		}
		lrcItems = $('p.lrc');
		activeLrcItems.removeClass('active');
		activeLrcItems = lrcItems.eq(0);
		activeLrcItems.addClass('active');
		$slideBox.css('bottom', 0);
	}
	
	function setAttribute() {
		var activeIndex = Math.floor(currentPos);
		activeLrcItems.removeClass('active');
		activeLrcItems = lrcItems.eq(activeIndex);
		activeLrcItems.addClass('active');
		for(var index in lrcItems) {
			var offset = (parseInt(index) + 0.5 - currentPos) * 2 / (maxLrcOnDisplay + 1);
			if(Math.abs(offset) < 1) {
				lrcItems.eq(index).css('opacity', textOpacityEasing(offset));
			} else {
				lrcItems.eq(index).css('opacity', 0);
			}
		}
		var offset = (-2.6- currentPos) * 2 / (maxLrcOnDisplay + 1);
		slideBox.children('.title').css('opacity', (Math.abs(offset) < 1) ? textOpacityEasing(offset) : 0);
		var offset = (-1.4 - currentPos) * 2 / (maxLrcOnDisplay + 1);
		slideBox.children('.artist').css('opacity', (Math.abs(offset) < 1) ? textOpacityEasing(offset) : 0);
		var offset = (-1.4 - currentPos) * 2 / (maxLrcOnDisplay + 1);
		slideBox.children('.album').css('opacity', (Math.abs(offset) < 1) ? textOpacityEasing(offset) : 0);
		var easingOffset = currentPos * (lrcItems.eq(1).offset().top - lrcItems.eq(0).offset().top);
		slideBox.css('bottom', easingOffset + 'px');
	}
	
	function displayLrc() {
		lrcState = 1;
		slideBox.empty();
		slideBox.append('<h1 class="title">' + songInfo.song_name + '</h1>');
		slideBox.append('<h3 class="artist">演唱：' + songInfo.artist + '</h3>');
		slideBox.append('<h3 class="album" style="display: none;">专辑：《' + songInfo.album + '》</h3>');
		slideBox.append('<hr />');
		startTime = songInfo.timestamp;
		currentPos = -3;
		initAttribute();
		setAttribute();
	}
	
	function refreshLrc() {
		if(lrcState == 1) {
			currentPos = getPosByTime((new Date().getTime()) - startTime);
			setAttribute();
		}
	}
	
	function onScroll (distance) {
		startTime += distance * timeOffsetPerScroll;
		refreshLrc();
	}
	
	function onError() {
		lrcState = 0;
		slideBox.empty();
		slideBox.append('<h2 class="error">对不起，没有找到对应的歌词。</h2>');
		slideBox.css('bottom', 0);
	}
	
	function onReceiveLrc (data) {
		try
		{
			lrcList = $.parseJSON(data).lyric;
			lrcList.sort(function (a, b) {
					return a.time - b.time;
				});
			if(lrcList.length == 0) { onError(); return; }
			lrcList.push({ lrc: '', time: 4294967295});
		} catch (e) {
			onError();
			return;
		}
		displayLrc();
	}
	
	$(document).ready(function () {
		
		slideBox = $('div#slide');
		lrcItems = $('p.lrc');
		activeLrcItems = lrcItems.eq(0);
		
		window.onmessage = function (event) {
			songInfo = $.parseJSON(event.data)
			$.post('q', songInfo, onReceiveLrc);
		}
		
		slideBox.mousewheel(function (event, delta) {
			onScroll(delta);
		});
		
		setInterval(refreshLrc, refreshInterval);
	});
})(jQuery);
