$('document').ready(function() {
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          }
      }
  });
  $(".object-action-button").click(function() {
    var objectID = $(this).attr("object-id");
    var objectName = $(this).attr("object-name");
    var objectType = $(this).attr("object-type");
    var objectAction = $(this).attr("object-action");
    var postActionURL = $(this).attr("post-action-url");
    var actionMethod = $(this).attr("action-method");
    var actionData = $(this).attr("action-data");

    if (!actionData) {
      actionData = "{}"
    }

    $("#formModalTitle").html("Sure?");
    $("#formModalBody").html("Are you sure you really want to "+objectAction+" "+objectType+" "+objectName+"?");
    $("#formModalSubmitButton").addClass("btn-success btn-default");
    $("#formModalSubmitButton").html("Yes!");
    $("#formModal").modal('show');

    $("#formModalSubmitButton").click(function() {
      $.ajax({
        url: '/api/'+objectType+'s/'+objectID+"/",
        data: $.parseJSON(actionData),
        type: actionMethod,
        success: function(result) {
          if(postActionURL) {
            $(location).attr("href", postActionURL);
          }
        },
        error: function(result, status, error) {
          alert("Error performing an action: "+status)
        }
      });
    });
  });
});
