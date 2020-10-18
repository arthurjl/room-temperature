"use strict";

(function() {

  window.addEventListener("load", init);

  function init() {
    const interval = setInterval(function() {
      udpateTherm1("#happy_button")
    }, 5000);

    qs("#happy_button").addEventListener("click", () => makePost("#happy_button"));
    qs("#sad_button").addEventListener("click", () => makePost("#sad_button"));
    qs("#angry_button").addEventListener("click", () => makePost("#angry_button"));
    qs("#confused_button").addEventListener("click", () => makePost("#confused_button"));
    qs("#neutral_button").addEventListener("click", () => makePost("#neutral_button"));
    qs("#slow_button").addEventListener("click", () => makePost("#slow_button"));
    qs("#fast_button").addEventListener("click", () => makePost("#fast_button"));

  }

  function makePost(id) {
    console.log("TYALDJSFLK DSTTHAT SD\n\n\n\n")
    let room_id = getRoomId(id)
    let url = "" + room_id + "/push";
    let params = new FormData();
    params.append("react", getReact(id))
    fetch(url, {method: "POST", body: params})
      .then(checkStatus)
      .then(response => response.json())
      .then(displayData)
      .catch(handleError);
  }

  function udpateTherm1(id) {
    console.log("What's up")
    let room_id = getRoomId(id)
    let param = "" + room_id + "/data";
    fetch(param)
      .then(checkStatus)
      .then(response => response.json())
      .then(displayData)
      .catch(handleError);
  }

  function getRoomId(id) {
    let val = qs(id).value
    console.log(val)
    return val
  }

  function getReact(id) {
    let val = qs(id).name
    console.log("GET REACT" + val)
    return val
  }
  
  function updateThermometer(temp) {
    console.log("UPDATING" + temp.result)
    qs(".thermometer2").style.height = temp.result + "%";
  }

  function displayData(data) {
    console.log(data)
    updateThermometer(data)
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