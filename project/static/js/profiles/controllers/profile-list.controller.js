(function () {
    'use strict';

    angular
        .module('stattrak.profiles.controllers')
        .controller('ProfileListController', ProfileListController);

    ProfileListController.$inject = ['$location', '$routeParams', 'Profile', 'Authentication', 'Snackbar'];

    function ProfileListController($location, $routeParams, Profile, Authentication, Snackbar) {
        var vm = this;
        vm.users = undefined;
        activate();

        function activate() {
            var authenticatedAccount = Authentication.getAuthenticatedAccount();
            // Redirect if not logged in
            if (!authenticatedAccount) {
                $location.url('/');
                Snackbar.error('You are not authorized to view this page.');
            }
            Profile.list().then(profileSuccess, profileError);

            function profileSuccess(data, status, headers, config) {
                vm.users = data.data;
            }

            function profileError(data, status, headers, config) {
                $location.url('/');
                Snackbar.error('No users found.');
            }

        }
    }
})();
