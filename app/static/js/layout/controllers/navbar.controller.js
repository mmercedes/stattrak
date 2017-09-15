(function () {
    'use strict';

    angular
        .module('stattrak.layout.controllers')
        .controller('NavbarController', NavbarController);

    NavbarController.$inject = ['$scope', 'Authentication'];

    function NavbarController($scope, Authentication) {

        function logout() {
            Authentication.logout();
        }
        var vm = this;

        vm.logout = logout;
    }
})();
