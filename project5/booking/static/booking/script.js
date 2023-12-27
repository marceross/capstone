document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (event) {
      var toggler = event.target.closest(".text-area-toggler");
      if (toggler) {
        event.preventDefault();
        var activityId = toggler.getAttribute("data-activity-id");
        toggleTextArea(activityId, toggler);
      }
    });
    
    function toggleTextArea(activityId, toggler) {
        var textArea = document.getElementById("text-area-" + activityId);
        var updateButton = document.querySelector(".update[data-activity-id='" + activityId + "']");
        
        if (textArea && updateButton) {
          if (textArea.style.display === "none" || textArea.style.display === "") {
            textArea.style.display = "block";
            toggler.style.display = "none";
            updateButton.style.display = "inline-block";
          } else {
            textArea.style.display = "none";
            toggler.style.display = "inline-block";
            updateButton.style.display = "none";
          }
        }
      }
    });


//funcion de live search
function showResult(str) {
  if (str.length==0) {
    document.getElementById("livesearch").innerHTML="";
    document.getElementById("livesearch").style.border="0px";
    return;
  }
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.onreadystatechange=function() {
    if (this.readyState==4 && this.status==200) {
      document.getElementById("livesearch").innerHTML=this.responseText;
      document.getElementById("livesearch").style.border="1px solid #A5ACB2";
    }
  }
  xmlhttp.open("GET","livesearch.php?q="+str,true);
  xmlhttp.send();
}



var xmlhttp = new XMLHttpRequest();
var url = "livesearch/?q=" + str;  // Update the URL

xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById("livesearch").innerHTML = this.responseText;
        document.getElementById("livesearch").style.border = "1px solid #A5ACB2";
    }
};

xmlhttp.open("GET", url, true);
xmlhttp.send();
    