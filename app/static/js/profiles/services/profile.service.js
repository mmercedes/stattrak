(function () {
    'use strict';

    angular
        .module('stattrak.profiles.services')
        .factory('Profile', Profile);

    Profile.$inject = ['$http'];

    function Profile($http) {

        var Profile = {
            destroy: destroy,
            get: get,
            update: update,
            list: list,
            getStats: getStats
        };

        return Profile;

        function destroy(profile) {
            return $http.delete('/api/v1/accounts/' + profile.id + '/');
        }

        function get(username) {
            return $http.get('/api/v1/accounts/' + username + '/');
        }

        function update(profile) {
            return $http.put('/api/v1/accounts/' + profile.username + '/', profile);
        }

        function list() {
            return $http.get('/api/v1/accounts/');
        }

        function getStats(username) {
            return $http.get('/api/v1/accounts/' + username + '/stats/');
        }

    }
})();
