
(function () {
    'use strict';

    function LoginController($location, $scope, Authentication) {

        function activate() {
            // If the user is authenticated, they should not be here.
            if (Authentication.isAuthenticated()) {
                $location.url('/');
            }
        }

        function login() {
            Authentication.login(vm.email, vm.password);
        }

        var vm = this;
        vm.login = login;
        activate();
    }

    LoginController.$inject = ['$location', '$scope', 'Authentication'];
    
    angular
        .module('stattrak.authentication.controllers')
        .controller('LoginController', LoginController);

})();

