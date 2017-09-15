(function () {
    'use strict';

    angular
        .module('stattrak.teams.controllers')
        .controller('TeamController', TeamController);

    TeamController.$inject = ['$location', '$routeParams', 'Team', 'Snackbar', 'Authentication'];

    function TeamController($location, $routeParams, Team, Snackbar, Authentication) {
        var vm = this;

        vm.team = undefined;
        activate();

        function activate() {
            var id = $routeParams.id.substr(0);
            
            if(!Authentication.isAuthenticated()){
                $location.url('/');
                Snackbar.error('You must be logged in to view this page.');
            }
            Team.get(id).then(teamSuccess, teamError);
            Team.getStats(id).then(statsSuccess, statsError);
            
            function teamSuccess(data, status, headers, config) {
                vm.team = data.data;
                console.log(vm.team);
            }
            function teamError(data, status, headers, config) {
                $location.url('/');
                Snackbar.error('Team does not exist.');
            }
            function statsSuccess(data, status, headers, config) {
                vm.stats = data.data;
            }
            function statsError(data, status, headers, config) {
                vm.stats = null;
            }
            

        }
    }

})();
