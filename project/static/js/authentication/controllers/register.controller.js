(function () {
    'use strict';

    angular
        .module('stattrak.authentication.controllers')
        .controller('RegisterController', RegisterController);

    RegisterController.$inject = ['$location', '$scope', 'Authentication'];

    function RegisterController($location, $scope, Authentication) {

        function activate() {
            // If the user is authenticated, they should not be here.
            if (Authentication.isAuthenticated()) {
                $location.url('/');
            }
        }
        
        function register() {
            Authentication.register(vm.email, vm.password, vm.username);
        }

        var vm = this;
        vm.register = register;
        activate();
    }
})();