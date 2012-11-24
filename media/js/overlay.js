$(function() {
    $(".overlaystep1 .steponebutton").on("click", function() {
	$(".overlaystep1").hide();
	$(".overlaystep2").show();
	$(".breadcrumb1").removeClass("currstep");
	$(".breadcrumb2").addClass("currstep");
    });
});

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

function scrapeImage(url, type) {
    $.post(scrapeImageURL,
          { 'url':url, 'type':type },
          function(response) {
              if (response.status == 'ok') {
                  $(".overlayimage").html(response.imgHTML);
		  $(".overlayimagecontainer").show();
                  $(".overlayslidedown").slideDown(500);
                  $("#overlayimagefile").val(response.filename);
                  $(".overlayimage img").Jcrop({
                      aspectRatio: 0.666666,
                      minSize: [ 80, 120 ],
                      setSelect: [ 0, 0, 80, 120 ],
                      addClass: 'jcrop-dark',
                      onSelect: setCoords
                  });
		  $(".cropbutton").show();
              } else {
                  alert('error');
              }
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
                  $(".overlayimage").html(response.imgHTML);
                  $(".overlayimagepath").val(response.filename);
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
