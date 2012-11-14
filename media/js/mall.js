$(function() {
    setSortable();
    $("#mall").on("click", ".storermv", function() {
	storeid = $(this).attr('id').substring(4);
	removeStore(storeid);
    });
    addformtrigger = $(".addstorecontainer").overlay({
	effect: 'apple',
	fixed: false,
	top: '20%',
	onBeforeLoad: function() {
	    $("#shield").show();
	},
	onClose: function() {
	    $("#shield").hide();
	}
    });
    $(".addstorebutton").on("click", function() {
	addStore();
    });
    $("#id_domain").on("change", function() {
	domain = $(this).val();
	// scrapeImage(domain);
	scrapeImage2();
    });
    $(".cropbutton").on("click", function() {
	doCrop();
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
//		  $(".addstoreformcontainer").hide();
	      } else {
		  showMessage($(".errorMsg"), response.errorMsg);
	      }
	  });
}
function scrapeImage(domain) {
    $.post(scrapeImageURL,
	  { 'domain':domain },
	  function(response) {
	      if (response.status == 'ok') {
		  $(".addstoreimage").html(response.imgHTML);
		  $(".addstoreimage img").Jcrop({
		      aspectRatio: 0.33333,
		      maxSize: [ 130, 390 ],
		      setSelect: [ 0, 390, 130, 390 ],
		      addClass: 'jcrop-dark',
		      onSelect: setCoords
		  });
	      } else {
		  alert('error');
	      }
	  });
}
function scrapeImage2() {
    $(".addstoreimage").html("<img src='/ssmedia/images/usrimg/1-tmp.jpg'>");
    $(".addstoreimage img").Jcrop({
	aspectRatio: 0.66666666,
	maxSize: [ 200, 300 ],
	setSelect: [ 0, 300, 200, 300 ],
	addClass: 'jcrop-dark',
	onSelect: setCoords
    });
}
function doCrop() {
    crop_x1 = $('#crop_x1').val();
    crop_y1 = $('#crop_y1').val();
    crop_x2 = $('#crop_x2').val();
    crop_y2 = $('#crop_y2').val();
    $.post(doCropURL,
	  { 'crop_x1':crop_x1, 'crop_y1':crop_y1, 'crop_x2':crop_x2, 'crop_y2':crop_y2 },
	  function(response) {
	      if (response.status == 'ok') {
		  $(".addstoreimage").html(response.imgHTML);
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
