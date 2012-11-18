function showMessage(el, msg) {
    $(".successMsg").text('').hide();
    $(".errorMsg").text('').hide();
    el.text(msg).show();
}
