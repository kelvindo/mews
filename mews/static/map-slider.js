$('#map-slider').slider();

var previous = 0

$("#map-slider").on("slide", function(slideEvt) {
  if (previous != slideEvt.value) {
    previous = slideEvt.value;
    var daysBefore = 30 - slideEvt.value;
    if (daysBefore != 1) {
      $('#slider-text').html(daysBefore + " Days Ago");
    } else {
      $('#slider-text').html(daysBefore + " Day Ago");
    }
    mapTimeDots(daysBefore);
  }
});