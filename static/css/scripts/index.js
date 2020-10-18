"use strict";
const swup = new Swup();

(function() {
	window.addEventListener("load", init);

	function init() {
		var btn = qs(".btn-light");
		btn.addEventListener('click', saveData);
	}

	function saveData(e) {
		e.preventDefault();
		var data = ui.classInput;
  	var str = data.value;
		localStorage.setItem('data', JSON.stringify(str));
		console.log("Saved class name to local storage")
	}

	/**
   * Returns first element matching selector.
   * @param {string} selector - CSS query selector.
   * @returns {object} - DOM object associated selector.
   */
  function qs(selector) {
    return document.querySelector(selector);
  }
})();