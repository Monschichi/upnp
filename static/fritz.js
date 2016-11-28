function prepad(number, length) {
  return(" ".repeat(Math.max(0,length-number.toString().length)) + number)
}

function myTimer() {
  $.getJSON( "/status", function( json ) {
    var contype = json.physical.type
    var indentlength = Math.max(4,contype.length)

    // Physical
    var physical = $("span#physical")
    physical.removeClass("fgred").text(contype + " ".repeat(indentlength-contype.length) + ":")
    var physicalstatus = $("<font></font>")
    if (json.physical.connected) {
      physicalstatus.addClass("fggreen").text("✔")
    } else {
      physicalstatus.addClass("fgred").text("✘")
    }
    physical.append(physicalstatus)
    var bw = $("<span></span>")
    bw.addClass("small").text(Math.round(json.physical.rate.up*8/1000000) + "/" + Math.round(json.physical.rate.down*8/1000000) + " MBit/s")
    physical.append(bw)

    // Logical
    var logical = $("span#logical")
    logical.text("CON" + " ".repeat(indentlength-3) + ":")
    var logicalstatus = $("<font></font>")
    if (json.logical.connected) {
      logicalstatus.addClass("fggreen").text("✔")
    } else {
      logicalstatus.addClass("fgred").text("✘" + json.logical.lasterror)
    }
    logical.append(logicalstatus)
    var ips = $("<span></span>")
    ips.addClass("small").text(json.logical.ipv4 + " " + json.logical.ipv6.prefix + "/" + json.logical.ipv6.length)
    logical.append(ips)

    // get rate lenght
    var maxrate = Math.max(Math.ceil(json.physical.rate.up/1024), Math.ceil(json.physical.rate.down/1024))
    var length = maxrate.toString().length + 3

    // UP
    // Text
    $("span#up").text("UP" + " ".repeat(indentlength-2) + ":" + prepad((json.rate.up/1024).toFixed(1),length) + "/" + Math.round(json.physical.rate.up/1024) + " kb/s")
    // Rate
    var uprate = json.rate.up/json.physical.rate.up*100
    $("span#up-bar").css("width", uprate + "%")
    if (uprate >= 90) {
      $("span#up-bar").addClass("bgred").removeClass("bgyellow bggreen")
    } else if (uprate >= 70) {
      $("span#up-bar").addClass("bgyellow").removeClass("bggreen bgred")
    } else {
      $("span#up-bar").addClass("bggreen").removeClass("bgyellow bgred")
    }

    // Down
    // Text
    $("span#down").text("DOWN" + " ".repeat(indentlength-4) + ":" + prepad((json.rate.down/1024).toFixed(1),length) + "/" + Math.round(json.physical.rate.down/1024) + " kb/s")
    // Rate
    var downrate = json.rate.down/json.physical.rate.down*100
    $("span#down-bar").css("width", downrate + "%")
    if (downrate >= 90) {
      $("span#down-bar").addClass("bgred").removeClass("bgyellow bggreen")
    } else if (downrate >= 70) {
      $("span#down-bar").addClass("bgyellow").removeClass("bggreen bgred")
    } else {
      $("span#down-bar").addClass("bggreen").removeClass("bgyellow bgred")
    }
  })
  .fail(function() {
      $("span#physical").addClass("fgred").removeClass("bgred bgyellow bggreen").text("error getting status")
      $("span#logical").text("")
      $("span#up").text("")
      $("span#down").text("")
      $("span#up-bar").css("width", "0%")
      $("span#down-bar").css("width", "0%")
  })
}

var reload = setInterval(myTimer, 1100)
