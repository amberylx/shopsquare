$(function() {
    setSortable();
    addwishlisttrigger = initOverlay($(".addwishlisticon"));
    $(".addtowishlistbutton").on("click", addToWishlist);
    $(".cropbutton").on("click", function() { doCrop('wishlist'); } );
    $("#wishlist").on("click", ".wlirmv", function() {
	wlitemid = $(this).attr('id').substring(4);
	removeWishlistitem(wlitemid);
    });
    $("#id_url").on("change", function() {
        url = $(this).val();
        scrapeImage(url, 'wishlist');
    });
});

function setSortable() {
    $(".wishlist").each(function() {
	$(this).sortable({
	    cursor:'move',
            cursorAt: {left:5},
            connectWith:'.wishlist',
            opacity:0.5,
            revert:true,
	    update: function(e, ui) {
	    }
	}).disableSelection();
    });
}

function loadWishlists(wishlistHTML) {
    $("#wishlist").html(wishlistHTML);
    setSortable();
}

function addToWishlist() {
    data = $("#addwishlistform").serialize();
    $.post(addToWishlistURL,
          data,
          function(response) {
	      if (response.status == 'ok') {
		  addwishlisttrigger.overlay().close();
		  showMessage($(".successMsg"), response.successMsg);
		  loadWishlists(response.wishlistHTML);
		  resetAddWishlistForm();
	      } else {
		  showMessage($(".errorMsg"), response.errorMsg);
	      }
          });
}
function resetAddWishlistForm() {
    $("#addwishlistform")[0].reset();
    $(".overlayimage").html("");
    $(".overlayimagecontainer").hide();
}

function removeWishlistitem(wlitemid) {
    $.post(removeWishlistitemURL,
	  { 'wlitemid':wlitemid },
	  function(response) {
	      if (response.status == 'ok') {
		  loadWishlists(response.wishlistHTML);
		  showMessage($(".successMsg"), response.successMsg);
	      } else {
		  showMessage($(".errorMsg"), response.errorMsg);
	      }
	  });
}
