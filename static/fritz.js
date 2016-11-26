function myTimer() {
  $.getJSON( "/status", function( json ) {
    if (json.physical.connected) {
      document.getElementById("dsl-status").style.color = '#00FF00';
      document.getElementById("dsl-status").innerHTML = '&#10004;';
    } else {
      document.getElementById("dsl-status").style.color = '#FF0000';
      document.getElementById("dsl-status").innerHTML = '&#10008;';
    }
    if (json.logical.connected) {
      document.getElementById("con-status").style.color = '#00FF00';
      document.getElementById("con-status").innerHTML = '&#10004;';
    } else {
      document.getElementById("con-status").style.color = '#FF0000';
      document.getElementById("con-status").innerHTML = '&#10008;';
    }

    document.getElementById("up").innerHTML = (json.rate.up/1024).toFixed(2);
    document.getElementById("down").innerHTML = (json.rate.down/1024).toFixed(2);

    var uprate = json.rate.up/json.physical.rate.up*100
    document.getElementById("up-bar").style.width = uprate + '%';
    if (uprate >= 90) {
      document.getElementById("up-bar").style.backgroundColor = '#FF0000';
    } else if (uprate >= 70) {
      document.getElementById("up-bar").style.backgroundColor = '#FFFF00';
    } else {
      document.getElementById("up-bar").style.backgroundColor = '#00FF00';
    }

    var downrate = json.rate.down/json.physical.rate.down*100
    document.getElementById("down-bar").style.width = downrate + '%';
    if (downrate >= 90) {
      document.getElementById("down-bar").style.backgroundColor = '#FF0000';
    } else if (downrate >= 70) {
      document.getElementById("down-bar").style.backgroundColor = '#FFFF00';
    } else {
      document.getElementById("down-bar").style.backgroundColor = '#00FF00';
    }
  })
  .fail(function() {
      document.getElementById("dsl-status").innerHTML = 'error getting status';
      document.getElementById("dsl-status").style.color = '#FF0000';
      document.getElementById("con-status").innerHTML = '&nbsp;';
      document.getElementById("up-bar").style.width = '0%';
      document.getElementById("down-bar").style.width = '0%';
  })
}

var reload = setInterval(myTimer, 1000);
