var DragAndDrop = function() {

    var _componentDragula = function() {
        dragula([document.getElementById('cards-target-left'), document.getElementById('cards-target-right')]);
    };

    return {
        init: function() {
            _componentDragula();
        }
    }
}();

document.addEventListener('DOMContentLoaded', function() {
    DragAndDrop.init();
});
