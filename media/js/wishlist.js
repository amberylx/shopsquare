$(function() {
    setSortable('wishlist', 'wli');
    addtowishlisttrigger = initOverlay($(".addtowishlisticon"));
    addwishlisttrigger = initOverlay($(".addwishlisticon"));
    $("#wishlist").on("click", ".wlirmv", function() {
	wlitemid = $(this).attr('id').substring(4);
	removeWishlistitem(wlitemid);
    });
    $(".overlay").on("change", "#id_url", function() {
        url = $(this).val();
	if (isValidURL(url)) {
	    imageScrapeCount = 0;
            scrapeImage(url, 'wishlist');
	}
    });
    $(".overlay").on("click", ".cropbutton", function() { doCrop('wishlist'); } );
    $(".overlay").on("click", ".addwishlistbutton", addWishlist);
    $(".overlay").on("click", ".addtowishlistbutton", addToWishlist);
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
    imgEl = $(".finalimg");
    data = $("#addtowishlistform").serialize();
    data += ("&width="+encodeURIComponent(imgEl.data("width")));
    data += ("&height="+encodeURIComponent(imgEl.data("height")));
    data += ("&filename="+encodeURIComponent(imgEl.data("filename")));
    $.post(addToWishlistURL,
          data,
          function(response) {
	      if (response.status == 'ok') {
		  addtowishlisttrigger.overlay().close();
		  showMessage($(".successMsg"), response.successMsg);
		  loadWishlists(response.wishlistHTML);
		  $("#addtowishlistoverlay").html(response.addToWishlistFormHTML);
	      } else {
		  showMessage($(".errorMsg"), response.errorMsg);
	      }
          });
}
/*
function resetAddtowishlistForm() {
    $("#addtowishlistform")[0].reset();
    $(".overlayimage").html("");
    $(".overlayimagecontainer").hide();
}*/

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
