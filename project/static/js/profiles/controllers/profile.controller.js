(function () {
    'use strict';

    angular
        .module('stattrak.profiles.controllers')
        .controller('ProfileController', ProfileController);

    ProfileController.$inject = ['$location', '$routeParams', 'Profile'];

    function ProfileController($location, $routeParams, Profile) {
        var vm = this;

        vm.profile = undefined;
        activate();

        function activate() {
            var username = $routeParams.username.substr(0);
            
            Profile.get(username).then(profileSuccess, profileError);

            function profileSuccess(data, status, headers, config) {
                vm.profile = data.data;
            }

            function profileError(data, status, headers, config) {
                $location.url('/');
                console.error('User does not exist.');
            }

        }
    }
})();
