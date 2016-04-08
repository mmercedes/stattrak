(function () {
    'use strict';

    angular
        .module('stattrak.teams.controllers')
        .controller('TeamListController', TeamListController);

    TeamListController.$inject = ['$location', '$routeParams', '$uibModal', 'Team', 'Authentication', 'Snackbar', 'League'];

    function TeamListController($location, $routeParams, $uibModal, Team, Authentication, Snackbar, League) {
        var vm = this;
        vm.league = undefined;
        vm.teams = undefined;
        vm.showModal = showModal;
        activate();
        
        function activate() {
            var authenticatedAccount = Authentication.getAuthenticatedAccount();
            // Redirect if not logged in
            Team.list().then(teamSuccess, teamError);
            League.get().then(leagueSuccess, leagueError);

            function teamSuccess(data, status, headers, config) {
                vm.teams = data.data;
            }

            function teamError(data, status, headers, config) {
                $location.url('/');
                Snackbar.error('No teams found.');
            }

            function leagueSuccess(data, status, headers, config) {
                vm.league = data.data[0];
            }

            function leagueError(data, status, headers, config) {
                Snackbar.error('League settings need to be updated! Contact an Admin!');
            }

        }

        function showModal() {
            
        }
    }
})();
