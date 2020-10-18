"use strict";
const swup = new Swup();

var btn = ui.btn;

(function() {
	window.addEventListener("load", init);

	function init() {
		btn.addEventListener('click', saveData);
	}

	function saveData(e) {
		e.preventDefault();
		var data = ui.classInput;
  	var str = data.value;
		localStorage.setItem('data', JSON.stringify(str));
		console.log("Saved class name to local storage")
	}
})();