/*
 */

function commit(redun_nmb, file_path, slice_id, prj_id) {
	$("#loading").fadeIn()
	$("#loading").text("Parsing PVNDL file...")
		var startc = new Date()
	$.post("/slices/commit", {
		redundancy : redun_nmb,
		path : file_path,
		project_id : prj_id
	}, function(data) {
		/* check data validity */
		$("#loading").append("Parse OK!")
		var endc = new Date()
		var diffc = endc-startc
		var diff_sc = Math.round(diffc % 60)
		alert(data+" Commit time = "+diff_sc+" segundos" )
		request(slice_id,file_path)
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
		var diff = end-start
		var diff_s = Math.round(diff % 60)
		alert(data+" Time = "+diff_s+" segundos" )
		$("#loading").fadeOut()
		$("#commit_img").attr('src', '/static/media/images/icons/true.png')
	});
};