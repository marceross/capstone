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

