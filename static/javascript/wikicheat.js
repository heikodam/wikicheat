// Some Code from https://codepen.io/Sahil89/pen/RQjyQa
// Some Code from https://medium.com/quick-code/simple-javascript-drag-drop-d044d8c5bed5

var container = document.getElementById("main");
var circle = document.querySelector("#loading");

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
    var start_title = document.getElementById("start_link");
    var end_title = document.getElementById("end_link");
    console.log(start_title.value)
    console.log("printed")
    // Both if statements not working
    if (start_title.value.length == 0 || end_title.value.length == 0){
      console.log("Error")
      show_error("*Please fill out both input fields")
    } else if(start_title.value ==  end_title.value){
      console.log("Error")
      show_error("*Please enter 2 differnet Wikipedia Titles")
    }
    
    else {
    positionCircle(e);
    start_loading()
    find_path()
    style_result()
    // end_loading()
    }
  }


  function style_result(){
    var start_title = document.getElementById("id-result-start_link");
    var end_title = document.getElementById("id-result-end_link");
    var arrow = document.getElementById("id-result-arrow");
    
    if ((start_title.innerHTML.length + end_title.innerHTML.length) > 23){
      start_title.className += " block";
      start_title.style.textAlign = " left";
      end_title.className += " block";
      end_title.style.textAlign = " right";
      arrow.className += " block rotate";

    }
  }


function find_path(){
  $.getJSON('/find_path', {
    "start_link": document.getElementById("start_link").value,
    "end_link": document.getElementById("end_link").value 
  }, function(data) {
    console.log(data)
    document.getElementById("wikicheat-div-result").style.display = "block";
    document.getElementById("id-result-start_link").innerHTML = data.start_link;
    document.getElementById("id-result-end_link").innerHTML = data.end_link;
    document.getElementById("span-distance").innerHTML = data.distance + " clicks";
    document.getElementById("span-runtime").innerHTML = data.time + "s";
    var wiki_icon = document.getElementById("wiki-icon");
    var loading = document.getElementById("loading");
    loading.style.display = "none";
    wiki_icon.style.display = "block"
    
  });
}

$("#wikicheat-form").submit(function(e) {
    e.preventDefault();
    positionCircle(e);
    start_loading()
    find_path()
    style_result()
    // end_loading()
});

function start_loading(){
  var wiki_icon = document.getElementById("wiki-icon");
  var loading = document.getElementById("loading");
  loading.style.display = "block";
  wiki_icon.style.display = "none"
}

function end_loading(){
  var wiki_icon = document.getElementById("wiki-icon");
  var loading = document.getElementById("loading");
  loading.style.display = "none";
  wiki_icon.style.display = "block"
}


function show_error(msg){
  var error = document.getElementById("error_message");
  error.innerHTML = msg;
  error.style.display = "block";
}
