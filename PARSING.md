script for parsing from epicurious.com


```js
// ==UserScript==
// @name         epicurious parser
// @namespace    http://tampermonkey.net/
// @version      2024-11-09
// @description  try to take over the world!
// @author       You
// @match        https://www.epicurious.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=epicurious.com
// @grant        none
// ==/UserScript==

function docReady(fn) {
    // see if DOM is already available
    if (document.readyState === "complete" || document.readyState === "interactive") {
        // call on next available tick
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

docReady((function() {
    const allLDS = (() => {
        const ld = document.querySelectorAll('script[type="application/ld+json"]')
        const results = []
        for (let i = 0; i < ld.length; i++) {
            results.push(JSON.parse(ld[i].innerText))
        }
        return results
    })()

    const preloadState = window.__PRELOADED_STATE__ ?? {}
    const result = window.SBPARSER ?? {
        lds: [],
        preloadState,
    }

    result.lds.push(...allLDS)

    fetch("https://sb-api.dowhile.uz/api/parsing/fetch-item/", {
        method: "POST",
        body: JSON.stringify({
            url: window.location.origin + window.location.pathname,
            raw_json: result
        }),
        headers: {
            "Content-Type": "application/json",
        },
    }).then(() => console.log("Otpravleno na server")).catch((e) => {console.log("VOZNIKLA OSHIBKA", e); console.error(e) })
}));
```