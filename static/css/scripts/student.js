"use strict";

(function() {

    window.addEventListener("load", init);

    function init() {
        let classname = qs("#classInput").value;
        qs(".class-color").textContent = classname;
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