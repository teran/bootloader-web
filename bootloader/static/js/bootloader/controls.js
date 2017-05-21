$('document').ready(function() {
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  });
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
        url: '/api/v1alpha2/'+objectType+'s/'+objectID+"/",
        data: $.parseJSON(actionData),
        type: actionMethod,
        success: function(result) {
          if(postActionURL) {
            $(location).attr("href", postActionURL);
          }
        },
        error: function(result, status, error) {
          console.error("Error performing an action: "+status)
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
    var formID = $(this).attr("form-id");
    var data = serializeFormToJSON($("#"+formID));
    var postActionURL = $(this).attr("post-action-url");
    var apiHandler = '/api/v1alpha2/'+$(this).attr('api-handler');

    $.ajax({
      url: apiHandler,
      data: data,
      type: 'POST',
      success: function(result) {
        $(location).attr("href", postActionURL)
      },
      error: function(result, status, error) {
        console.error("status: "+status+" ; "+JSON.stringify(result));
      }
    });
  });
  $("form").submit(function() {
    $(this).preventDefault();
  });
  $(".upload-profile-button").click(function() {
    var formData = new FormData();
    var profileName = $('#profile-name').val();
    var profileVersion = $('#profile-version').val();
    formData.append('yaml', $('input[type=file]')[0].files[0]);

    $.ajax({
      url: '/tools/yaml2json',
      data: formData,
      contentType: false,
      processData: false,
      type: 'POST',
      success: function(data) {
          var profileObject = {
            'name': profileName,
            'version': profileVersion,
            'profile': JSON.stringify(data),
          };
          $.ajax({
            url: '/api/v1alpha2/profiles/',
            type: 'POST',
            data: profileObject,
            success: function(result) {
              $(location).attr("href", "/deployments/profiles.html")
            },
            error: function(result, status, error) {
              console.error("status: "+status+" ; "+JSON.stringify(result));
            }
          });
      },
      error: function(result, status, error) {
        console.error("status: "+status+" ; "+JSON.stringify(result));
      }
    });
  });
  $("div.deployment-progress-dynamic").css("width", function() {
    var deploymentID = $(this).attr("deployment-id");
    setInterval(function() {
      $.ajax({
        url: '/api/v1alpha2/deployments/'+deploymentID,
        contentType: false,
        processData: false,
        type: 'GET',
        success: function(data){
          $("div#deployment-"+deploymentID).css("width", data["progress"]+"%");
          $("div#deployment-"+deploymentID).attr("aria-valuenow", data["progress"]);
        },
        error: function(result, status, error) {
          console.error("status: "+status+" ; "+JSON.stringify(result));
        }
      });
    }, 3000);
  });
});
