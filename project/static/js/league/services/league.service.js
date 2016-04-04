(function () {
    'use strict';

    angular
        .module('stattrak.league.services')
        .factory('League', League);

    League.$inject = ['$http'];

    function League($http) {

        var League = {
            get: get,
            update: update
        };

        return League;

        function get() {
            return $http.get('/api/v1/league/');
        }

        function update(league) {
            return $http.put('/api/v1/league/', league);
        }

    }
})();
