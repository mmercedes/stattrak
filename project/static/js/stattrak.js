(function () {
    'use strict';

    angular
        .module('stattrak', [
            'stattrak.routes',
            'stattrak.authentication',
            'stattrak.config',
            'stattrak.layout',
            'stattrak.profiles',
            'stattrak.utils',
            'stattrak.league'
        ]);

    angular
        .module('stattrak.routes', ['ngRoute']);

    angular
        .module('stattrak.config', []);
    
    angular
        .module('stattrak')
        .run(run);
    
    run.$inject = ['$http'];
    
    function run($http) {
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';
    }
})();
