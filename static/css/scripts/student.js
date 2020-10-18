"use strict";

(function() {

    window.addEventListener("load", init);

    function init() {
        var stored = JSON.parse(localStorage.getItem('data'));
        console.log(stored);
        qs(".class-color").textContent = stored;
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