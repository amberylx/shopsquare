$(function() {
    setSortable();
    addformtrigger = initOverlay($(".addstorecontainer"));
    $(".addstorebutton").on("click", addStore);
    $(".cropbutton").on("click", function() { doCrop('store'); } );
    $("#mall").on("click", ".storermv", function() {
	storeid = $(this).attr('id').substring(4);
	removeStore(storeid);
    });
    $("#id_domain").on("change", function() {
	domain = $(this).val();
	scrapeImage(domain, 'store');
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
		if (oldfloorid == newfloorid) {
		    // if store's new floor is same as old floor, moved store within same floor
		    oldfloororder = getFloororderFromFloorid(oldfloorid);
		    newfloororder = getFloorOrder(newfloorid);
		    moveStore(storeid, 'samefloor', oldfloorid, oldfloororder, newfloorid, newfloororder);		    
		} else {
		    // moved store from another floor
		    thisfloorid = getFlooridFromEl(this);
		    if (newfloorid != thisfloorid) {
			// only trigger move store for update event for new floor
			oldfloororder = getFloororderFromFloorid(oldfloorid);
			newfloororder = getFloorOrder(newfloorid);
			moveStore(storeid, 'difffloor', oldfloorid, oldfloororder, newfloorid, newfloororder);
		    }
		}
	    },
	}).disableSelection();
    });
}

function loadMall(mallHTML) {
    $("#mall").html(mallHTML);
    setSortable();
}

/* add store */
function addStore() {
    data = $('#addstoreform').serialize();
    data += ("&mallid="+encodeURIComponent(mallid));
    $.post(addStoreURL,
	  data,
	  function(response) {
	      if (response.status == 'ok') {
		  addformtrigger.overlay().close();
		  showMessage($(".successMsg"), response.successMsg);
		  loadMall(response.mallHTML);
		  resetAddStoreForm();
	      } else {
		  showMessage($(".errorMsg"), response.errorMsg);
	      }
	  });
}
function resetAddStoreForm() {
    $("#addstoreform")[0].reset();
    $(".overlayimage").html("");
    $(".overlayimagecontainer").hide();
}

/* move store */
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
function moveStore(storeid, movetype, oldfloorid, oldfloororder, newfloorid, newfloororder) {
    data = {
	'mallid':mallid,
	'storeid':storeid,
	'movetype':movetype,
	'oldfloorid':oldfloorid,
	'oldfloororder':oldfloororder,
	'newfloorid':newfloorid,
	'newfloororder':newfloororder
    }
    $.post(moveStoreURL,
	   data,
	   function(response) {
	       if (response.status == 'ok') {
		   loadMall(response.mallHTML);
	       } else {
		   showMessage($(".errorMsg"), response.errorMsg);
		   loadMall(response.mallHTML);
	       }
	   });
}

function removeStore(storeid) {
    $.post(removeStoreURL,
	  { 'mallid':mallid, 'storeid':storeid },
	  function(response) {
	      if (response.status == "ok") {
		  loadMall(response.mallHTML);
		  showMessage($(".successMsg"), response.successMsg);
	      } else {
		  showMessage($(".errorMsg"), response.errorMsg);
	      }
	  });
}
