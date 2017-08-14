$("table tr td #es").on("click",function(e){
		e.preventDefault();
			$.ajax({
				type:'GET',
				url:$(this).attr("href"),
				beforeSend:Espera,
				success:function(resp){
					$("#FormAjax").html(resp);
				}
			});
			 function Espera(){
		      $("#FormAjax").html('<img src="/static/img/log.gif" id="icono"></img><br>Procesando...');
		    }
	});	
	$("table tr td #v").on("click",function(e){
		$.ajax({
			type:'GET',
			url:$(this).attr("href"),
			success:function(resp){
				$(".modal-body").html(resp);
			}
		});
	});