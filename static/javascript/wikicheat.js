// function allowDrop(ev) {
//     ev.preventDefault();
//   }
  
//   function drag(ev) {
//     ev.dataTransfer.setData("text", ev.target.id);
//   }
  
//   function drop(ev) {
//     alert("Droped in Main")
//     // ev.preventDefault();
//     // var data = ev.dataTransfer.getData("text");
//     // ev.target.appendChild(document.getElementById("main"));
//   }

var container = document.getElementById("main");
var circle = document.querySelector(".circle");

TweenMax.set(".section", {
  backgroundColor: function() {
    return Math.random() * 0xffffff;
  }
});

TweenMax.set(circle, { scale: 0, xPercent: -50, yPercent: -50 });

container.addEventListener("pointerenter", function(e) {
  TweenMax.to(circle, 0.3, { scale: 1, opacity: 1 });
  positionCircle(e);
});

container.addEventListener("pointerleave", function(e) {
  TweenMax.to(circle, 0.3, { scale: 0, opacity: 0 });
  positionCircle(e);
});

container.addEventListener("pointermove", function(e) {
  positionCircle(e);
});

function positionCircle(e) {
  var rect = container.getBoundingClientRect();  
  var relX = e.pageX - container.offsetLeft;
  var relY = e.pageY - container.offsetTop;

  TweenMax.to(circle, 0.3, { x: relX, y: relY });
}
