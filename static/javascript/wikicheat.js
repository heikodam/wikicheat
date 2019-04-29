// Some Code from https://codepen.io/Sahil89/pen/RQjyQa
// Some Code from https://medium.com/quick-code/simple-javascript-drag-drop-d044d8c5bed5

var container = document.getElementById("main");
var circle = document.querySelector(".start-button");

function positionCircle(e) {
  // var rect = container.getBoundingClientRect();  
  // var relX = e.pageX - container.offsetLeft;
  // var relY = e.pageY - container.offsetTop;
  var relX = e.clientX - container.offsetLeft;
  var relY = e.clientY - container.offsetTop;

  TweenMax.to(circle, 1, { x: relX, y: relY });
}


function allowDrop(e) {
    e.preventDefault();
  }
  
  function drag(e) {
    // positionCircle(e);
  }
  
  function drop(e) {
    // document.getElementById("myP").style.cursor = "pointer";
    positionCircle(e);
    document.getElementById('submit-btn').click();
    // $.post( "/postmethod", {
    //   javascript_data: data 
    //   });
  }


  window.onload = function(){
    var start_title = document.getElementById("id-result-start_link");
    var end_title = document.getElementById("id-result-end_link");
    var arrow = document.getElementById("id-result-arrow");
    
    if ((start_title.innerHTML.length + end_title.innerHTML.length) > 23){
      // Change css Class
      // start_title.classList.add("block left");
      // end_title.classList.add("block right");
      start_title.className += " block";
      start_title.style.textAlign = " left";
      end_title.className += " block";
      end_title.style.textAlign = " right";
      arrow.className += " block rotate";

    }
  }