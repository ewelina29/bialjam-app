/**
 * Created by boska on 19.12.17.
 */
$( document ).ready(function() {

function readURL(input) {
    console.log("ddd");
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    console.log("ddd2");

    reader.onload = function(e) {
      $('#img-def').attr('src', e.target.result);
    };
    console.log("ddd3");

    reader.readAsDataURL(input.files[0]);
  }
}

$("#files").change(function() {
  readURL(this);
});
});