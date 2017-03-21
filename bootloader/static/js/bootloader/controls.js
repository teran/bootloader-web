$('document').ready(function() {
  $(".delete-object").click(function() {
    var objectID = $(this).attr("object-id");
    var objectName = $(this).attr("object-name");
    var objectType = $(this).attr("object-type");
    var postActionURL = $("#post-action-url").val();

    $("#formModalTitle").html("Sure?");
    $("#formModalBody").html("Are you sure you really want to delete "+objectType+" "+objectName+"?");
    $("#formModalSubmitButton").addClass("btn-danger btn-default");
    $("#formModalSubmitButton").html("Delete");
    $("#formModal").modal('show');
    $("#formModalSubmitButton").click(function() {
      $.ajax({
        url: '/api/'+objectType+'s/'+objectID+"/",
        type: 'DELETE',
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
