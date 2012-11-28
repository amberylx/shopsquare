$(function() {
    $(".step1button").on("click", function() {
	transitionToStep(1, 2);
    });
    $(".back2button").on("click", function() {
	transitionToStep(2, 1);
    });
    $(".nextimage").on("click", function() {
	currImgEl = $("#visibleimage");
	killJcrop(currImgEl);
	currImgEl.removeClass("visibleimage").addClass("hiddenimage").removeAttr('id');

	nextImgEl = currImgEl.next();
	nextImgEl.removeClass("hiddenImage").addClass("visibleimage").attr('id', 'visibleimage');
	initJcrop(nextImgEl);
    });
});

function transitionToStep(oldstep, newstep) {
    oldstepButton = ".step"+oldstep+"button";
    overlayOldStepClass = ".overlaystep"+oldstep;
    overlayNewStepClass = ".overlaystep"+newstep;
    overlayOldBreadcrumbClass = ".breadcrumb"+oldstep;
    overlayNewBreadcrumbClass = ".breadcrumb"+newstep;

    $(overlayOldStepClass).hide();
    $(overlayNewStepClass).show();
    $(overlayOldBreadcrumbClass).removeClass("currstep");
    $(overlayNewBreadcrumbClass).addClass("currstep");
}

function initOverlay(trigger) {
    t = trigger.overlay({
        effect: 'apple',
        fixed: false,
        top: '15%',
        onBeforeLoad: function() {
            $("body").addClass("overlayOpen");
        },
        onClose: function() {
            $("body").removeClass("overlayOpen");
        }
    });
    return t;
}
function initJcrop(imgEl) {
    imgEl.Jcrop({
        aspectRatio: 0.666666,
        minSize: [ 80, 120 ],
        setSelect: [ 0, 0, 80, 120 ],
        addClass: 'jcrop-dark',
        onSelect: setCoords
    }, function () {
	imgEl.data("jcrop", this);
    });
}
function killJcrop(imgEl) {
    jcropapi = imgEl.data("jcrop");
    jcropapi.destroy();
    imgEl.attr('style', '');
}

var imageScrapeCount = 0;
function scrapeImage(url, type, start_index) {
    var imgindex;
    $(".loadingicon").show();
    $.ajax({
	type: 'POST',
	url: scrapeImageURL,
        data: { 'url':url, 'type':type, 'start_index':start_index },
	success: function(response) {
	    imgindex = response.imgindex;
            if (response.status == 'ok') {
		imgContainer = $(".overlayimage");
                imgContainer.append(response.imgHTML);

		// first image scraped
		var imgEl = imgContainer.children().last();
		imgEl.data("filename", response.filename);
		if (imgContainer.hasClass("noimages")) {
		    imgContainer.removeClass("noimages");
		    $(".overlayimagecontainer").show();
		    $(".cropbutton").show();
                    $(".overlayslidedown").slideDown(500);
		    imgEl.removeClass("hiddenimage").addClass("visibleimage").attr('id', 'visibleimage');
		    initJcrop(imgEl);
		}

		// keep scraping
		imageScrapeCount += 1;
		if (imageScrapeCount < 2) {
		    scrapeImage(url, type, response.imgindex);
		}
            } else if (response.status == 'complete') {
		alert('complete');
	    } else {
                alert('error');
            }
        }
    }).done(function() {
	$(".loadingicon").hide();
    });
}
function doCrop(type) {
    crop_x1 = $('#crop_x1').val();
    crop_y1 = $('#crop_y1').val();
    crop_x2 = $('#crop_x2').val();
    crop_y2 = $('#crop_y2').val();
    filename = $("#visibleimage").data("filename");
    $.post(doCropURL,
          { 'crop_x1':crop_x1, 'crop_y1':crop_y1, 'crop_x2':crop_x2, 'crop_y2':crop_y2, 'filename':filename, 'type':type },
          function(response) {
              if (response.status == 'ok') {
                  $(".overlayimage").html(response.imgHTML);
                  $("#overlayimagefile").val(response.filename);
		  $(".cropbutton").hide();
              } else {
                  alert('error');
              }
          })
}
function setCoords(c) {
    $('#crop_x1').val(c.x);
    $('#crop_y1').val(c.y);
    $('#crop_x2').val(c.x2);
    $('#crop_y2').val(c.y2);
}
