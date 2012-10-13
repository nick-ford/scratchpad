$(function(){
  $('#js-container').masonry({
    // options
    itemSelector : '.item',
    columnWidth : function(containerWidth) {
      return containerWidth / 5;
    }
  });
  $('#js-container').jsquares();
});
