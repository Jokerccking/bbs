var log = function() {
	console.log.apply(console, arguments);
};

var e = function(ele) {
	return document.querySelector(ele);
};

var ajax = function(method, path, data, callBack){
	var r = new XMLHttpRequest();
	r.open(method, path, true);
	r.setRequestHeader("Content-Type", "application/json");
	r.onreadystatechange = function(){
		if(r.readyState === 4) {
			callBack(r.response)
		}
	};

	data  = JSON.stringify(data);
	r.send(data);
};


var timeString = function(timestamp) {
	t = new Date(timestamp * 1000);
	t = t.toLocaleTimeString();
	return t;
};

var bindClickEvent = function(ele, func) {
	ele.addEventListener("click", func);
};
