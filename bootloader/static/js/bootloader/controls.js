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
  function serializeFormToJSON(form) {
    var formData = form.serializeArray();
    var arrangedData = {};
    $.each(formData, function(idx, el) {
      arrangedData[el.name] = el.value;
    });

    return arrangedData
  }
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
  $(".modal-action-button").click(function() {
    var modalID = $(this).attr("modal-id");
    var modalAction = $(this).attr("modal-action");

    $("#"+modalID).modal(modalAction);
  });
  $(".send-form").click(function() {
    var data = serializeFormToJSON($("#new-deployment-form"));
    var postActionURL = "/deployments/deployments.html";

    console.log(data);
    $.ajax({
      url: '/api/deployments/',
      data: data,
      type: 'POST',
      success: function(result) {
        $(location).attr("href", postActionURL)
      },
      error: function(result, status, error) {
        alert("status: "+status+" ; "+JSON.stringify(result));
      }
    });
  });
});
