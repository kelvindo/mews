$('#map-slider').slider();

var previous = 30

$("#map-slider").on("slide", function(slideEvt) {
  if (previous != slideEvt.value) {
    previous = slideEvt.value;
    var daysBefore = 30 - slideEvt.value;

    mapTimeDots(daysBefore);
  }
});