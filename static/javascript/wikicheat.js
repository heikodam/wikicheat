function allowDrop(e) {
  e.preventDefault();
}

function drag(e) {
// what to do on drag

}

function drop(e) {
  check_submit();
}

wiki_icon = document.getElementById("wiki-icon");
wiki_icon.addEventListener('touchend', function(){
  check_submit();
}, false)

$("#wiki-icon").on("tap", function(){
  check_submit();
})


function find_path(){
$.getJSON('/find_path', {
  "start_link": document.getElementById("start_link").value.replace(" ", "_").toLowerCase(),
  "end_link": document.getElementById("end_link").value.replace(" ", "_").toLowerCase() 
}, function(data) {
  if (data.error){
    show_error(data.error)
    end_loading()
  } else {
    document.getElementById("wikicheat-div-result").style.display = "block";
    document.getElementById("id-result-start_link").innerHTML = data.start_link.replace("_", " ");
    document.getElementById("id-result-end_link").innerHTML = data.end_link.replace("_", " ");
    document.getElementById("span-distance").innerHTML = data.distance + " clicks";
    document.getElementById("span-runtime").innerHTML = data.time + "s";
    var wiki_icon = document.getElementById("wiki-icon");
    var loading = document.getElementById("loading");
    loading.style.display = "none";
    wiki_icon.style.display = "block"
    style_result() 
    end_loading()
  }   
});
}

$("#wikicheat-form").submit(function(e) {
    e.preventDefault();
    check_submit();
});

function check_submit(){
  var start_title = document.getElementById("start_link");
  var end_title = document.getElementById("end_link");
  if (start_title.value.length == 0 || end_title.value.length == 0){
    show_error("*Please fill out both input fields")
  } else if(start_title.value.toLowerCase() ==  end_title.value.toLowerCase()){
    show_error("*Please enter 2 differnet Wikipedia Titles")
  }

  else {
  remove_error()
  start_loading()
  find_path()
  }
}

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

function remove_error(){
  var error = document.getElementById("error_message");
  error.style.display = "none";
}


function positionLoading(e) {
  var container = document.getElementById("main");
  var loading = document.querySelector("#loading");

  var relX = e.clientX - container.offsetLeft;
  var relY = e.clientY - container.offsetTop;

  TweenMax.to(loading, 1, { x: relX, y: relY });
}



function style_result(){
  var start_title = document.getElementById("id-result-start_link");
  var end_title = document.getElementById("id-result-end_link");
  var arrow = document.getElementById("id-result-arrow");

  if ((start_title.innerHTML.length + end_title.innerHTML.length) > 18){
    
    start_title.className += " block";
    start_title.style.textAlign = " left";
    end_title.className += " block";
    end_title.style.textAlign = " right";
    arrow.className += " block rotate";

  }
}