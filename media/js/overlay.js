$(function() {
    $(".overlay").on("click", ".step1button", function() {
	transitionToStep(1, 2);
    });
    $(".overlay").on("click", ".step2button", function() {
	var selectimg = $(".overlayimages img.selectimage");
	var img = $('<img class="cropimg">');
	img.attr('src', selectimg.attr('src'));
	
	$(".overlaycropimg").append(img);
	$("#overlayimagefile").val(selectimg.data("filename"));
	initJcrop($(".cropimg"));
	transitionToStep(2, 3);
    });
    $(".overlay").on("click", ".back3button", function() {
	killJcrop($(".cropimg"));
	$('.cropimg').remove();
	transitionToStep(3, 2);
    });
    $(".overlay").on("click", ".back2button", function() {
	transitionToStep(2, 1);
    });
    $(".overlay").on("click", ".overlayimages img", function() {
	$(".selectimage").removeClass("selectimage");
	$(this).addClass("selectimage");
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
		imgContainer = $(".overlayimages");
                imgContainer.append(response.imgHTML);

		// first image scraped
		var imgEl = imgContainer.children().last();
		imgEl.data("filename", response.filename);
		if (imgContainer.hasClass("noimages")) {
		    imgContainer.removeClass("noimages");
		    $(".overlayimages").show();
                    $(".overlayslidedown").slideDown(500);
		    //initJcrop(imgEl);
		}

		// keep scraping
		imageScrapeCount += 1;
		if (imageScrapeCount < 3) {
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
    filename = $("#overlayimagefile").val();
    $.post(doCropURL,
          { 'crop_x1':crop_x1, 'crop_y1':crop_y1, 'crop_x2':crop_x2, 'crop_y2':crop_y2, 'filename':filename, 'type':type },
          function(response) {
              if (response.status == 'ok') {
                  $(".overlayimages").html(response.imgHTML);
                  $("#overlayimagefile").val(response.filename);
		  killJcrop($(".cropimg"));
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
