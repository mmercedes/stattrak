(function () {
    'use strict';

    angular
        .module('stattrak.results.services')
        .factory('Results', Results);

    Results.$inject = ['$http'];

    function Results($http) {

        var Results = {
            get: get,
            list: list,
            add: add,
            addPlayerData: addPlayerData,
            addTeamData: addTeamData,
            getPlayerData: getPlayerData,
            getTeamData: getTeamData
        };

        return Results;

        function list() {
            return $http.get('/api/v1/results/');
        }

        function get(id) {
            return $http.get('/api/v1/results/'+ id +'/');
        }
        
        function add(result) {
            return $http.post('/api/v1/results/', result);
        }

        function addPlayerData(data) {
            return $http.post('/api/v1/playerData/', data);
        }

        function addTeamData(data) {
            return $http.post('/api/v1/teamData/', data);
        }

        function getPlayerData(id) {
            return $http.get('/api/v1/playerData/' + id +'/')
        }

        function getTeamData(id) {
            return $http.get('/api/v1/teamData/' + id +'/')
        }
    }
})();
