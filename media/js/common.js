function showMessage(el, msg) {
    $(".successMsg").text('').hide();
    $(".errorMsg").text('').hide();
    el.text(msg).show();
}

/* functions for sorting/moving items */
function getIdFromEl(el, prefix) {
    return $(el).attr('id').substring(prefix.length);
}
function getCurrOrder(sortableEl, sortableKey) {
    return sortableEl.sortable("serialize", { key: sortableKey });
}
function getNewOrder(sortableEl, key) {
    return sortableEl.data(key);
}

function setSortable(container, item) {
    containerPrefix = container + '_';
    containerClass = '.' + container;
    containerIdPrefix = '#' + container + '_';
    itemPrefix = item + '_';

    $(containerClass).each(function(index) {
        var oldcontainerid;
        $(this).sortable({
            cursor:'move',
            cursorAt: {left:5},
            connectWith: containerClass,
            opacity:0.5,
            revert:true,
            start: function(e, ui) {
                // get store's current floor
                oldcontainerid = getIdFromEl(ui.item.parent(), containerPrefix);
                // get floor's current order
                $(this).data("oldorder", getCurrOrder($(containerIdPrefix+oldcontainerid), item));
            },
            update: function(e, ui) {
                itemid = getIdFromEl(ui.item, itemPrefix);
                newcontainerid = getIdFromEl(ui.item.parent(), containerPrefix);
                if (oldcontainerid == newcontainerid) {
                    // if store's new floor is same as old floor, moved store within same floor
                    oldorder = getNewOrder($(containerIdPrefix+oldcontainerid), "oldorder");
                    neworder = getCurrOrder($(containerIdPrefix+newcontainerid), item);
                    moveItem(itemid, 'same', oldcontainerid, oldorder, newcontainerid, neworder);
                } else {
                    // moved store from another floor
                    thiscontainerid = getIdFromEl(this, containerPrefix);
                    if (newcontainerid != thiscontainerid) {
                        // only trigger move store for update event for new floor
                        oldorder = getNewOrder($(containerIdPrefix+oldcontainerid), "oldorder");
                        neworder = getCurrOrder($(containerIdPrefix+newcontainerid), item);
                        moveItem(itemid, 'diff', oldcontainerid, oldorder, newcontainerid, neworder);
                    }
                }
            }
        }).disableSelection();
    });
}

function moveItem(itemid, movetype, oldcontainerid, oldorder, newcontainerid, neworder) {
    data = {
        'mallid':(typeof(mallid) == 'undefined' ? '' : mallid),
        'itemid':itemid,
        'movetype':movetype,
        'oldcontainerid':oldcontainerid,
        'oldorder':oldorder,
        'newcontainerid':newcontainerid,
        'neworder':neworder
    }
    $.post(moveItemURL,
           data,
           function(response) {
	       moveItemCallback(response);
           });
}

function loadHTML(el, html, loadHTMLcallback) {
    $(el).html(html);
    loadHTMLcallback();
}
