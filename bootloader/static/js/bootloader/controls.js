$(".delete-server").click(function() {
  var objectID = $(this).attr("object-id");
  var objectName = $(this).attr("object-name");
  var postActionURL = $("#post-action-url").val();

  if(objectID && objectName && confirm("Delete server "+objectName+"?")) {
    $.ajax({
      url: '/api/servers/'+objectID+"/",
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
  }
})
