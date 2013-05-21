/*
 */
function addController(cc_id, pj_id) {
	$("#loading-btn").attr('src', '/static/images/icons/loading.gif')
	$("#plus_link").attr('style', 'cursor:default;')
	$.get("/controllers/new/" + cc_id + "/" + pj_id, function(data) {
		window.location.reload()
	});
	return false;
};

function commit(file_path, slice_id, prj_id) {
	$("#loading").fadeIn()
	$("#loading").text("Parsing VXDL file...")
	var startc = new Date()
	$.post("/slices/commit", {
		path : file_path,
		project_id : prj_id
	}, function(data) {
		if (data.split(' ')[0] == 'ERROR!') {
			$("#loading").fadeOut()
			alert('Error while parsing VXDL:\n'+data)
		} else {
			/* check data validity */
			$("#loading").append("Parse OK!")
			var endc = new Date()
			var diffc = endc - startc
			var diff_sc = Math.round(diffc % 60)
			//alert(data + " Commit time = " + diff_sc + " segundos")
			request(slice_id, file_path)
		}
	});
	return false;
};

function request(sliceid, file_path) {
	var start = new Date()
	$("#loading").append("</ br> Sending request to VIP...")

	$.post("/slices/request_to_vip", {
		slice_id : sliceid,
		path : file_path
	}, function(data) {
		/*TODO check data validity */
		$("#loading").append("</ br> Request Done")
		var end = new Date()
		var diff = end - start
		var diff_s = Math.round(diff % 60)
		//alert(data + " Time = " + diff_s + " segundos")
		$("#loading").fadeOut()
		$("#commit_img").attr('src', '/static/images/icons/true.png')
	});
};