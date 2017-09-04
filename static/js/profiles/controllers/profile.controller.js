(function () {
    'use strict';

    angular
        .module('stattrak.profiles.controllers')
        .controller('ProfileController', ProfileController);

    ProfileController.$inject = ['$location', '$routeParams', 'Profile', 'Snackbar', 'Authentication'];

    function ProfileController($location, $routeParams, Profile, Snackbar, Authentication) {
        var vm = this;

        vm.profile = undefined;
        vm.makeAdmin = makeAdmin;
        activate();

        function activate() {
            var username = $routeParams.username.substr(0);
            
            if(!Authentication.isAuthenticated()){
                $location.url('/');
                Snackbar.error('You must be logged in to view this page.');
            }
            vm.user = Authentication.getAuthenticatedAccount();

            Profile.get(username).then(profileSuccess, profileError);
            Profile.getStats(username).then(statsSuccess, statsError);
            
            function profileSuccess(data, status, headers, config) {
                vm.profile = data.data;
            }
            function profileError(data, status, headers, config) {
                $location.url('/');
                Snackbar.error('User does not exist.');
            }
            function statsSuccess(data, status, headers, config) {
                vm.stats = data.data;
                console.log(vm.stats);
            }
            function statsError(data, status, headers, config) {
                vm.stats = null;
            }
            

        }

        function makeAdmin() {
            vm.profile.is_admin = true;
            Profile.update(vm.profile).then(adminSuccess, adminError);

            function adminSuccess(data, status, headers, config) {
                Snackbar.show('Success');
            }
            function adminError(data, status, headers, config) {
                Snackbar.show('An error occured.');
            }            
        }
    }
})();
