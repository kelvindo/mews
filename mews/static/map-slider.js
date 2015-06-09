$('#map-slider').slider();

var previous = 0

$("#map-slider").on("slide", function(slideEvt) {
  var daysBefore = 30 - slideEvt.value;
  if (previous != daysBefore) {
    previous = daysBefore;
    if (daysBefore != 1) {
      $('#slider-text').html(daysBefore + " Days Ago");
    } else {
      $('#slider-text').html(daysBefore + " Day Ago");
    }
    mapTimeDots(daysBefore);
  }
});