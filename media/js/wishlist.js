$(function() {
    addwishlisttrigger = initOverlay($(".addwishlisticon"));
    $(".addtowishlistbutton").on("click", addToWishlist);
    $(".cropbutton").on("click", doCrop);
    $("#id_url").on("change", function() {
        url = $(this).val();
        scrapeImage(url);
    });
});

function addToWishlist() {
    data = $("#addwishlistform").serialize();
    $.post(addToWishlistURL,
          data,
          function(response) {
	      if (response.status == 'ok') {
		  addwishlisttrigger.overlay().close();
		  showMessage($(".successMsg"), response.successMsg);
		  //loadWishlist();
		  resetWishlistForm();
	      } else {
		  showMessage($(".errorMsg"), response.errorMsg);
	      }
          });
}
function resetAddWishlistForm() {
    $("#addwishlistform")[0].reset();
    $(".overlayimage").html("");
    $(".overlayimagecontainer").html("").hide();
}
