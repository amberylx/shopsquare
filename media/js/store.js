$(function() {
    setSortable('floor', 'store');
    addformtrigger = initOverlay($(".addstoreicon"));
    $("#mall").on("click", ".storermv", function() {
        storeid = $(this).attr('id').substring(4);
        removeStore(storeid);
    });
    $("#floor").on("click", ".storermv", function() {
        storeid = $(this).attr('id').substring(4);
        removeStore(storeid);
    });
    $(".overlay").on("change", "#id_url", function() {
        url = $(this).val();
	if (isValidURL(url)) {
	    imageScrapeCount = 0;
            scrapeImage(url, 'store', 0);
	}
    });
    $(".overlay").on("click", ".cropbutton", function() { doCrop('store'); } );
    $(".overlay").on("click", ".addstorebutton", addStore);
/*    $("input").on("change", function() {
	if (isNotBlank(this)) {
	    $(this).next("span.statusicon").show();
	} else {
	    $(this).next("span.statusicon").hide();
	}
    });*/
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
    imgEl = $(".finalimg");
    data = $('#addstoreform').serialize();
    data += ("&mallid="+encodeURIComponent(mallid));
    data += ("&width="+encodeURIComponent(imgEl.data("width")));
    data += ("&height="+encodeURIComponent(imgEl.data("height")));
    data += ("&filename="+encodeURIComponent(imgEl.data("filename")));
    $.post(addStoreURL,
	  data,
	  function(response) {
	      if (response.status == 'ok') {
		  addformtrigger.overlay().close();
		  showMessage($(".successMsg"), response.successMsg);
		  loadHTML(response.html);
		  $("#addstoreoverlay").html(response.addStoreFormHTML);
	      } else {
		  showMessage($(".errorMsg"), response.errorMsg);
	      }
	  });
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
