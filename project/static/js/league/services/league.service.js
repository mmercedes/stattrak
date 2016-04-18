(function () {
    'use strict';

    angular
        .module('stattrak.league.services')
        .factory('League', League);

    League.$inject = ['$http'];

    function League($http) {

        var League = {
            get: get,
            update: update,
            listPlayerFields: listPlayerFields,
            listTeamFields: listTeamFields,
            addPlayerField: addPlayerField,
            addTeamField: addTeamField
        };

        return League;

        function get() {
            return $http.get('/api/v1/league/');
        }

        function update(league) {
            return $http.post('/api/v1/league/', league);
        }

        function listPlayerFields() {
            return $http.get('/api/v1/playerDataTypes/')
        }

        function listTeamFields() {
            return $http.get('/api/v1/teamDataTypes/')
        }

        function addPlayerField(data) {
            return $http.post('/api/v1/playerDataTypes/', data)
        }

        function addTeamField(data) {
            return $http.post('/api/v1/teamDataTypes/', data)
        }
    }
})();
