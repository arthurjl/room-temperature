"use strict";

(function() {

  window.addEventListener("load", init);

  function init() {
    qs(".button").addEventListener("click", clickTemp);
  }

  function clickTemp() {
    let param = "/_stuff";
    fetch(param)
      .then(checkStatus)
      .then(response => response.json())
      .then(displayYips)
      .catch(handleError);

  }

  /**
   * returns the response's text if successful and throws an error otherwise
   * @param {object} response - text to check for success or failure
   * @returns {object} - successful response
   */
  function checkStatus(response) {
    if (!response.ok) {
      throw Error("Error in request: " + response.statusText);
    }
    return response;
  }

  /**
   * displays an error message if an error occurs at any point in the program.
   */
  function handleError() {
    console.log("error");
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