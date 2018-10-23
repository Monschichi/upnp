/*eslint max-len: ["error", { "code": 140 }]*/

function prepad(number, length) {
    return (" ".repeat(Math.max(0, length - number.toString().length)) + number);
}

function uhr() {
    let Jetzt = new Date();
    let datum = {weekday: "short", day: "numeric", month: "short"};
    $("span#datum").text(Jetzt.toLocaleDateString("de-DE", datum));
    $("span#uhr").text(Jetzt.toLocaleTimeString("de-DE"));
}

function fail(jqxhr, textStatus, error) {
    console.log("Status failed: " + textStatus + " " + error);
    $("span#physical").addClass("fgred").removeClass("bgred bgyellow bggreen")
        .text("error getting status");
    $("span#logical").text("");
    $("span#up").text("");
    $("span#down").text("");
    $("span#up-bar").css("width", "0%");
    $("span#down-bar").css("width", "0%");
}

function up_down_text(updown, indentlength, json, length) {
    let indent = indentlength - updown.length;
    $("span#" + updown).text(
        updown.toUpperCase() + " ".repeat(indent) + ":" + prepad((json["rate"][updown] / 1024).toFixed(1), length) + "/" +
        Math.round(json["physical"]["rate"][updown] / 1024) + " kb/s");
}

function up_down_rate(upbar, uprate) {
    upbar.css("width", uprate + "%");
    if (uprate >= 90) {
        upbar.addClass("bgred").removeClass("bgyellow bggreen");
    } else if (uprate >= 70) {
        upbar.addClass("bgyellow").removeClass("bggreen bgred");
    } else {
        upbar.addClass("bggreen").removeClass("bgyellow bgred");
    }
}

function status_icon(json, type) {
    let status = $("<span></span>");
    if (json[type]["connected"]) {
        status.addClass("fggreen").text("✔");
    } else {
        status.addClass("fgred").text("✘");
    }
    return status;
}

function status_text(type, contype, indentlength, json) {
    let span = $("span#" + type);
    let indent = indentlength - contype.length;
    span.removeClass("fgred").text(contype + " ".repeat(indent) + ":");
    span.append(status_icon(json, type));
    let bw = $("<span></span>");
    if (type === "physical") {
        bw.addClass("small").text(
            Math.round(json["physical"]["rate"]["up"] * 8 / 1000000) + "/" + Math.round(json["physical"]["rate"]["down"] * 8 / 1000000) +
            " MBit/s");
    } else {
        bw.addClass("small")
            .text(json["logical"]["ipv4"] + " " + json["logical"]["ipv6"]["prefix"] + "/" + json["logical"]["ipv6"]["length"]);
    }
    span.append(bw);
}

function update(json) {
    let contype = json["physical"]["type"];
    let indentlength = Math.max(4, contype.length);

    // Physical
    status_text("physical", contype, indentlength, json);

    // Logical
    status_text("logical", "CON", indentlength, json);

    // get rate lenght
    let maxrate = Math.max(Math.ceil(json["physical"]["rate"]["up"] / 1024), Math.ceil(json["physical"]["rate"]["down"] / 1024));
    let length = maxrate.toString().length + 3;

    // UP
    // Text
    up_down_text("up", indentlength, json, length);
    // Rate
    up_down_rate($("span#up-bar"), json["rate"]["up"] / json["physical"]["rate"]["up"] * 100);

    // Down
    // Text
    up_down_text("down", indentlength, json, length);
    // Rate
    up_down_rate($("span#down-bar"), json["rate"]["down"] / json["physical"]["rate"]["down"] * 100);
}

function myTimer() {
    $.getJSON("/status", function (json) {
        update(json);
    }).fail(function (jqxhr, textStatus, error) {
        fail(jqxhr, textStatus, error);
    });
    uhr();
}

setInterval(myTimer, 1001);
