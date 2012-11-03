$(function() {
    setSortable();
    $(".addstorecontainer").on("click", function() {
	$(".addstoreformcontainer").slideDown(500);
    });
    $(".storermv").on("click", function() {
	storeid = $(this).attr('id').substring(4);
	removeStore(storeid);
    });
 });

function setSortable() {
    $(".floor").each(function(index) {
	var oldfloorid;
	$(this).sortable({
	    cursor:'move',
	    cursorAt: {left:5},
	    connectWith:'.floor',
	    opacity:0.5,
	    revert:true,
	    start: function(e, ui) {
		// get store's current floor
		oldfloorid = getFlooridFromEl(ui.item.parent());
		// get floor's current order
		$(this).data("oldfloororder", getFloorOrder(oldfloorid));
	    },
	    update: function(e, ui) {
		storeid = getStoreidFromEl(ui.item);
		newfloorid = getFlooridFromEl(ui.item.parent());
		// if store's new floor is same as old floor, moved store within same floor
		oldfloororder = getFloororderFromFloorid(oldfloorid);
		newfloororder = getFloorOrder(newfloorid);
		moveStore(storeid, oldfloorid, oldfloororder, newfloorid, newfloororder);
	    },
	}).disableSelection();
    });
}

function getFloororderFromFloorid(floorid) {
    return $('#floor_'+floorid).data("oldfloororder");
}
function getFlooridFromEl(el) {
    return $(el).attr('id').substring(6);
}
function getStoreidFromEl(el) {
    return $(el).attr('id').substring(6);
}
function getFloorOrder(floorid) {
    return $("#floor_"+floorid).sortable("serialize", { key:'store' });
}
function moveStore(storeid, oldfloorid, oldfloororder, newfloorid, newfloororder) {
    data = {
	'mallid':mallid,
	'storeid':storeid,
	'oldfloorid':oldfloorid,
	'oldfloororder':oldfloororder,
	'newfloorid':newfloorid,
	'newfloororder':newfloororder
    }
    $.post(moveStoreURL,
	   data,
	   function(response) {
	   });
}

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

