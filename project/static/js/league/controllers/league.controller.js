(function () {
    'use strict';

    angular
        .module('stattrak.league.controllers')
        .controller('LeagueController', LeagueController);

    LeagueController.$inject = ['$location', '$routeParams', 'League', 'Snackbar', 'Authentication'];

    function LeagueController($location, $routeParams, League, Snackbar, Authentication) {
        var vm = this;

        vm.league = undefined;
        vm.update = update;
        activate();

        function activate() {
            if(!Authentication.isAuthenticated()){
                $location.url('/');
                Snackbar.error('You must be logged in to view this page.');
            }
            vm.user = Authentication.getAuthenticatedAccount();
            if(!vm.user.is_admin){
                $location.url('/');
                Snackbar.error('You must be an admin to view this page.');
            }
            
            League.get().then(leagueSuccess, leagueError);
            
            function leagueSuccess(data, status, headers, config) {
                vm.league = data.data;
            }

            function leagueError(data, status, headers, config) {
                vm.league = { 'teamSize': 0, 'name': null, 'logo': null }
            }
        }

        function update() {
                League.update(vm.league).then(leagueSuccess, leagueError);

                function leagueSuccess(data, status, headers, config) {
                    Snackbar.show('League settings have been updated.');
                }

                function leagueError(data, status, headers, config) {
                    Snackbar.error(data.error);
                }
        }

    }
})();
