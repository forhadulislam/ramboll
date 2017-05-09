$(document).ready(function(){
	$(".selectpicker").click(function(){
		//alert('asdasd');
	});
	
	$.get("http://127.0.0.1:5000/api/v1/get-stopid", function(data, status){
        console.log(data)
    });
});