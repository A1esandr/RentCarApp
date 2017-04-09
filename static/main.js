// js scripts

(function($){
$(document).ready(function(){

	function loadAuto() {
		$.ajax({
			url: '/getauto',
			method: "GET",
			error: function(){alert("При загрузке произошла ошибка");},
			success: function(data){
				
			}
		}).done(function(data) {
			var el = document.getElementById('rentCar');
			if(el){
				el.innerHTML = '';
				el.innerHTML = "<option disabled selected value>-- Автомобиль --</option>"+data;
			}
			var el = document.getElementById('historyCar');
			if(el){
				el.innerHTML = '';
				el.innerHTML = "<option disabled selected value>-- Автомобиль --</option>"+data;
			}
		});
	}
	loadAuto();

	$.ajax({
		url: '/getplace',
		method: "GET",
		error: function(){alert("При загрузке произошла ошибка");},
		success: function(data){
			
		}
	}).done(function(data) {
		var el = document.getElementById('rentStartPlace');
		if(el){
			el.innerHTML = '';
			el.innerHTML = "<option disabled selected value>-- Пункт взятия --</option>"+data;
		}
		var el = document.getElementById('rentFinishPlace');
		if(el){
			el.innerHTML = '';
			el.innerHTML = "<option disabled selected value>-- Пункт возврата --</option>"+data;
		}
	});

	$.ajax({
		url: '/getbrand',
		method: "GET",
		error: function(){alert("При загрузке произошла ошибка");},
		success: function(data){
			
		}
	}).done(function(data) {
		var el = document.getElementById('autoBrand');
		if(el){
			el.innerHTML = '';
			el.innerHTML = "<option disabled selected value>-- Марка --</option>"+data;
		}
	});

	//input mask
	$('#rentBegDate').inputmask({"mask": "99-99-9999"});
	$('#rentEndDate').inputmask({"mask": "99-99-9999"});

	$('#addRentButton').click(function(){
		$('#addRentModal').modal('toggle');
	});
	$('#submitRent').click(function(){
		var rent = {};
		rent.Car = $('#rentCar option:selected').val();
		rent.Renter = $('#rentRenter').val();
		rent.BegDate = $('#rentBegDate').val();
		rent.EndDate = $('#rentEndDate').val();
		rent.StartPlace = $('#rentStartPlace option:selected').val();
		rent.FinishPlace = $('#rentFinishPlace option:selected').val();
		rent.addrent = '1'
		
		var jqxhr = $.ajax({
			url: '/rent',
			method: "POST",
			data: rent,
			dataType: "text",
			error: function(){alert("При сохранении произошла ошибка");},
			success: function(data){
				
			}
		}).done(function(data) {
			$('#refreshButton').trigger('click');
			$('#addRentModal').modal('hide');
			$('#successModal').modal('show');
		});
	});

	$('#addAutoButton').click(function(){
		$('#addAutoModal').modal('toggle');
	});
	$('#submitAuto').click(function(){
		var auto = {};
		auto.Brand = $('#autoBrand option:selected').val();
		auto.AutoNumber = $('#autoNumber').val();
		auto.addauto = '1'
		
		var jqxhr = $.ajax({
			url: '/auto',
			method: "POST",
			data: auto,
			dataType: "text",
			error: function(){alert("При сохранении произошла ошибка");},
			success: function(data){
				
			}
		}).done(function(data) {
			loadAuto();
			$('#addAutoModal').modal('hide');
			$('#successModal').modal('show');
		});
	});

	$('#refreshButton').click(function(){
		var car = $('#historyCar option:selected').val();
		var jqxhr = $.ajax({
			url: '/',
			method: "POST",
			data: {history:"1",car:car},
			dataType: "text",
			error: function(){alert("При загрузке произошла ошибка");},
			success: function(data){
				
			}
		}).done(function( data ) {
			var el = document.getElementById('rentTableBody');
			if(el){
				el.innerHTML = '';
				el.innerHTML = data;
			}
			var jqxhr2 = $.ajax({
				url: '/brand',
				method: "GET",
				error: function(){alert("При загрузке произошла ошибка");},
				success: function(data){
					
				}
			}).done(function( data ) {
				var el = document.getElementById('brandTableBody');
				if(el){
					el.innerHTML = '';
					el.innerHTML = data;
				}
				var jqxhr3 = $.ajax({
					url: '/place',
					method: "GET",
					error: function(){alert("При загрузке произошла ошибка");},
					success: function(data){
						
					}
				}).done(function( data ) {
					var el = document.getElementById('placeTableBody');
					if(el){
						el.innerHTML = '';
						el.innerHTML = data;
					}
				});
			});
		});
	});
	$('#refreshCarButton').click(function(){
		$('#historyCar').val('');
		$('#refreshButton').trigger('click');
	});
	$('#addRentModal').on('hidden.bs.modal', function (e) {
		$('.addRentField').val('');
		$('body').css('padding-right','0px');
	});
	$('#addAutoModal').on('hidden.bs.modal', function (e) {
		$('.addAutoField').val('');
		$('body').css('padding-right','0px');
	});
	$('#refreshButton').trigger('click');
});
})(jQuery);
