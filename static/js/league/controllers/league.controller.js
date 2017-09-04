(function () {
    'use strict';

    angular
        .module('stattrak.league.controllers')
        .controller('LeagueController', LeagueController);

    LeagueController.$inject = ['$location', '$routeParams', 'League', 'Snackbar', 'Authentication'];

    function LeagueController($location, $routeParams, League, Snackbar, Authentication) {
        var vm = this;

        vm.league = undefined;
        vm.playerFields = undefined;
        vm.teamFields = undefined;
        vm.newPlayerField = '';
        vm.newTeamField = '';
        vm.update = update;
        vm.addPlayerField = addPlayerField;
        vm.addTeamField = addTeamField;
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
            League.listPlayerFields().then(playerSuccess, playerError);
            League.listTeamFields().then(teamSuccess, teamError);
            
            function leagueSuccess(data, status, headers, config) {
                vm.league = data.data[0];
            }

            function leagueError(data, status, headers, config) {
                vm.league = { 'teamSize': 0, 'name': null, 'logo': null }
            }

            function playerSuccess(data, status, headers, config) {
                vm.playerFields = data.data;
            }

            function playerError(data, status, headers, config) {
                Snackbar.error('Error getting player fields.');
            }

            function teamSuccess(data, status, headers, config) {
                vm.teamFields = data.data;
            }

            function teamError (data, status, headers, config) {
                Snackbar.error('Error getting team fields.');
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

        function addPlayerField() {
            League.addPlayerField({'key': vm.newPlayerField}).then(playerSuccess, playerError);

            function playerSuccess(data, status, headers, config) {
                vm.playerFields.push(data.data);
                vm.newPlayerField = '';
            }
            function playerError(data, status, headers, config) {
                Snackbar.error('Error adding field.')
            }
        }

        function addTeamField() {
            League.addTeamField({'key': vm.newTeamField}).then(teamSuccess, teamError);

            function teamSuccess(data, status, headers, config) {
                vm.teamFields.push(data.data);
                vm.newTeamField = '';
            }
            function teamError(data, status, headers, config) {
                Snackbar.error('Error adding field.')
            }
        }        

    }
})();
