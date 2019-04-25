window.onload = function(){
    var start_title = document.getElementById("id-mr-start_link");
    var end_title = document.getElementById("id-mr-end_link");
    var arrow = document.getElementById("id-mr-arrow");
    
    if ((start_title.innerHTML.length + end_title.innerHTML.length) > 0){
      // Change css Class
      start_title.className += " block";
      start_title.style.textAlign = " left";
      end_title.className += " block";
      end_title.style.textAlign = " right";
      arrow.className += " block rotate";

    }
  }