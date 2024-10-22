odoo.define('client_vault.script', function (require) {
    "use strict";
    const rpc = require('web.rpc');
    let observerInitialized = false;

    function addButtonClickListeners() {
        if (observerInitialized) {
            return;
        }

        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    var vaultBTNs = document.querySelectorAll('.vault');
                    if (vaultBTNs.length > 0) {
                        vaultBTNs.forEach(function(vaultBTN) {
                            if (!vaultBTN.getAttribute('data-click-listener')) {
                                vaultBTN.addEventListener('click', function() {
                                    console.log('btn clické');
                                });
                                vaultBTN.setAttribute('data-click-listener', 'true');
                            }
                        });
                        observer.disconnect();
                    }
                }
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });
        observerInitialized = true;
    }
    var model = 'res.partner';
    var domain = [];
    var fields = [];
    rpc.query({
        model: model,
        method: 'search_read',
        args: [domain, fields],
    }).then(function(data){
        console.log(data);
    })
    document.addEventListener('DOMContentLoaded', function() {
        console.log('dom loaded');
        if (document.body) {
            addButtonClickListeners();
        } else {
            console.error('document.body is not available');
        }
    });


});