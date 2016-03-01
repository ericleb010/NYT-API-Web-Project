// By: Eric Leblanc

var DRIVE = 0;
var FUSION = 1;
var AI = 2;
var SPACE = 3;

$(document).ready(function() {

	//Display the main page's snippet.
	displayMainSnippet(DRIVE);
	displayMainSnippet(FUSION);
	displayMainSnippet(AI);
	displayMainSnippet(SPACE);

	$("#apply-theme").click(function() {
		var text = $("#theme-select option:selected").val();

		$.ajax({
			type: "GET",
			data: { theme: text },
			url: "/theme_update",
			success: function() {
				location.reload();
			}
		});

	});
});



var displayMainSnippet = function(topic) {
	$.ajax({
		type: "GET",
		url: "/articles/" + topic + "/1",
		success: function(data) {
			switch (topic) {
				case DRIVE:
					$("#vehicle-insert").html(data);
					break;
				case FUSION:
					$("#fusion-insert").html(data);
					break;
				case AI:
					$("#ai-insert").html(data);
					break;
				case SPACE:
					$("#space-insert").html(data);
					break;
			}
		}
	});
}	
