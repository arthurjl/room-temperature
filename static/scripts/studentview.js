"use strict";

(function() {

  window.addEventListener("load", init);

  function init() {
    updateBigFace()
    udpateTherm1("#happy_button")

    const interval = setInterval(function() {
      udpateTherm1("#happy_button")
      updateBigFace()
    }, 5000);

    qs("#happy_button").addEventListener("click", () => makePost("#happy_button"));
    qs("#sad_button").addEventListener("click", () => makePost("#sad_button"));
    qs("#angry_button").addEventListener("click", () => makePost("#angry_button"));
    qs("#surprised_button").addEventListener("click", () => makePost("#surprised_button"));
    qs("#neutral_button").addEventListener("click", () => makePost("#neutral_button"));
    qs("#slow_button").addEventListener("click", () => makePost("#slow_button"));
    qs("#fast_button").addEventListener("click", () => makePost("#fast_button"));

  }

  function updateBigFace() {
    let room_id = getRoomId("#happy_button");
    let param = "" + room_id + "/active";

    fetch(param)
      .then(checkStatus)
      .then(response => response.json())
      .then((data) => {
        console.log("YEEEEE" + data)
        qs('#biggest-face').src = "/static/images/" + data.result + ".png";
      })
      .catch(handleError);
  }

  function makePost(id) {
    console.log("posting to emotion");
    let room_id = getRoomId(id);
    let params = new FormData();
    params.append("room_id", room_id);
    let react_id = getReact(id);
    let reaction;
    if (react_id == 0) {
      reaction = "happy";
    } else if (react_id == 1) {
      reaction = "neutral";
    } else if (react_id == 2) {
      reaction = "sad";
    } else if (react_id == 3) {
      reaction = "angry";
    } else {
      reaction = "surprised";
    }
    params.append(reaction, 1.0)
    let url = "../emotions"
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
    console.log("YAYAAYAY " + param)
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