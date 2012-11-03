$(function() {
    $("#mall").sortable();
    $("#floor_1").sortable({
	cursor:'move',
	cursorAt: {left:5},
	containment:'parent',
	forcePlaceholderSize: true,
	// placeholder:'sortable-placeholder',
	//grid: [100,150]
	helper:'clone',
	opacity:0.5,
	revert:true,
	update: function(e, ui) {
	    getStoreOrder();
	}
    });
    $(".addstorecontainer").on("click", function() {
	$(".addstoreformcontainer").slideDown(500);
    });
    $(".storermv").on("click", function() {
	storeid = $(this).attr('id').substring(4);
	removeStore(storeid);
    });
 });

function removeStore(storeid) {
    $.post(removeStoreURL,
	  { 'mallid':mallid, 'storeid':storeid },
	  function(response) {
	      if (response.status == "ok") {
		  alert(response.successMsg);
	      } else {
		  alert(response.errorMsg);
	      }
	  });
}

function getStoreOrder() {
    hash = $("#floor_1").sortable("serialize", { key:'store' });
}
