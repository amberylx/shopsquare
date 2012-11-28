$(function() {
    setSortable('floor', 'store');
    addformtrigger = initOverlay($(".addstoreicon"));
    $(".addstorebutton").on("click", addStore);
    $(".cropbutton").on("click", function() { doCrop('store'); } );
    $("#mall").on("click", ".storermv", function() {
        storeid = $(this).attr('id').substring(4);
        removeStore(storeid);
    });
    $("#floor").on("click", ".storermv", function() {
        storeid = $(this).attr('id').substring(4);
        removeStore(storeid);
    });
    $("#id_url").on("change", function() {
        url = $(this).val();
	if (isValidURL(url)) {
            scrapeImage(url, 'store', 0);
	}
    });
    $("input").on("change", function() {
	if (isNotBlank(this)) {
	    $(this).next("span.statusicon").show();
	} else {
	    $(this).next("span.statusicon").hide();
	}
    });
});

function loadHTML(html) {
    if (viewmode == 'mall') {
	$("#mall").html(html);
    } else if (viewmode == 'floor') {
	$("#floor").html(html);
    }
    setSortable('floor', 'store');
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
		  loadHTML(response.html);
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
function moveItemCallback(response) {
    loadHTML(response.html);
    if (response.status == 'error') {
	showMessage($(".errorMsg"), response.errorMsg);
    }
}

function removeStore(storeid) {
    if (viewmode == 'mall') {
	data = { 'mallid':mallid, 'storeid':storeid }
    } else if (viewmode == 'floor') {
	data = { 'mallid':mallid, 'storeid':storeid, 'floorid':floorid }
    }

    $.post(removeStoreURL,
	   data,
	   function(response) {
	       if (response.status == "ok") {
		   loadHTML(response.html);
		   showMessage($(".successMsg"), response.successMsg);
	       } else {
		   showMessage($(".errorMsg"), response.errorMsg);
	       }
	   });
}
