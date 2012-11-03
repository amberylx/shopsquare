$(function() {
    $("#mall").sortable();
    $("#floor1").sortable({
	cursor:'move',
	cursorAt: {left:5},
	containment:'parent',
	forcePlaceholderSize: true,
	// placeholder:'sortable-placeholder',
	//grid: [100,150]
	helper:'clone',
	opacity:0.5,
	revert:true
    });
    $(".addstorecontainer").on("click", function() {
	$(".addstoreformcontainer").slideDown(500);
    });
});
