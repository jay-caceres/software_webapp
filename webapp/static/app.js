$(document).ready(function (){
	$('#gals_req, #date, #price, #tot').change(function(){
		if($("#gals_req").val().length && $("#date").val().length && $("#tot").val().length && $("#price").val().length){
				$("#sub").prop('disabled', false);
		} else {
				$("#sub").prop('disabled', true);
		}
	});
});