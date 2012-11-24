$(function() {
    setSortable('wishlist', 'wli');
    addtowishlisttrigger = initOverlay($(".addtowishlisticon"));
    $(".addtowishlistbutton").on("click", addToWishlist);
    addwishlisttrigger = initOverlay($(".addwishlisticon"));
    $(".addwishlistbutton").on("click", addWishlist);
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

function loadWishlists(wishlistHTML) {
    $("#wishlist").html(wishlistHTML);
    setSortable('wishlist', 'wli');
}

function addWishlist() {
    data = $("#addwishlistform").serialize();
    $.post(addWishlistURL,
	   data,
	   function(response) {
	       if (response.status == 'ok') {
		  addwishlisttrigger.overlay().close();
		  showMessage($(".successMsg"), response.successMsg);
		  loadWishlists(response.wishlistHTML);
		  resetAddwishlistForm();
	       } else {
		  showMessage($(".errorMsg"), response.errorMsg);
	       }
	   });
}
function resetAddwishlistForm() {
    $("#addwishlistform")[0].reset();
}
function addToWishlist() {
    data = $("#addtowishlistform").serialize();
    $.post(addToWishlistURL,
          data,
          function(response) {
	      if (response.status == 'ok') {
		  addtowishlisttrigger.overlay().close();
		  showMessage($(".successMsg"), response.successMsg);
		  loadWishlists(response.wishlistHTML);
		  resetAddtowishlistForm();
	      } else {
		  showMessage($(".errorMsg"), response.errorMsg);
	      }
          });
}
function resetAddtowishlistForm() {
    $("#addtowishlistform")[0].reset();
    $(".overlayimage").html("");
    $(".overlayimagecontainer").hide();
}

/* move wishlistitem */
function moveItemCallback(response) {
    loadWishlists(response.html);
    if (response.status == 'error') {
        showMessage($(".errorMsg"), response.errorMsg);
    }
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
