(function () {
    'use strict';

    angular
        .module('stattrak.teams.services')
        .factory('Team', Team);

    Team.$inject = ['$http'];

    function Team($http) {

        var Team = {
            destroy: destroy,
            get: get,
            update: update,
            list: list
        };

        return Team;

        function destroy(team) {
            return $http.delete('/api/v1/teams/' + team.id + '/');
        }

        function get(id) {
            return $http.get('/api/v1/teams/' + id + '/');
        }

        function update(team) {
            return $http.post('/api/v1/teams/' + team.id + '/', team);
        }

        function list() {
            return $http.get('/api/v1/teams/');
        }

    }
})();
