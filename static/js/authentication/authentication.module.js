(function () {
    'use strict';

    angular
        .module('stattrak.authentication', [
            'stattrak.authentication.controllers',
            'stattrak.authentication.services'
        ]);

    angular
        .module('stattrak.authentication.controllers', []);

    angular
        .module('stattrak.authentication.services', ['ngCookies']);
})();
