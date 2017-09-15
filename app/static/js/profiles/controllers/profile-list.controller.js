(function () {
    'use strict';

    angular
        .module('stattrak.profiles.controllers')
        .controller('ProfileListController', ProfileListController);

    ProfileListController.$inject = ['$location', '$routeParams', 'Profile', 'Authentication', 'Snackbar', 'League'];

    function ProfileListController($location, $routeParams, Profile, Authentication, Snackbar, League) {
        var vm = this;
        vm.league = undefined;
        vm.users = undefined;
        activate();

        function activate() {
            var authenticatedAccount = Authentication.getAuthenticatedAccount();
            // Redirect if not logged in
            Profile.list().then(profileSuccess, profileError);
            League.get().then(leagueSuccess, leagueError);

            function profileSuccess(data, status, headers, config) {
                vm.users = data.data;
            }

            function profileError(data, status, headers, config) {
                Snackbar.error('No users found.');
            }

            function leagueSuccess(data, status, headers, config) {
                vm.league = data.data[0];
            }

            function leagueError(data, status, headers, config) {
                Snackbar.error('League settings need to be updated! Contact an Admin!');
            }

        }
    }
})();
