$(function() {
    $("#addtowishlistbutton").on("click", addToWishlist);
});

function addToWishlist() {
    data = $("#addwishlistform").serialize();
    $.post(addToWishlistURL,
          data,
          function(response) {
          });
}
