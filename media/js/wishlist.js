$(function() {
    $("#addtowishlistbutton").on("click", addToWishlist);
    addwishlisttrigger = initOverlay($(".addwishlisticon"));
});

function addToWishlist() {
    data = $("#addwishlistform").serialize();
    $.post(addToWishlistURL,
          data,
          function(response) {
          });
}
