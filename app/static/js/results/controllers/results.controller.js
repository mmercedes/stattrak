(function () {
    'use strict';

    angular
        .module('stattrak.results.controllers')
        .controller('ResultsController', ResultsController);

    ResultsController.$inject = ['$location', '$routeParams', 'Results', 'League', 'Snackbar', 'Authentication', 'Team'];

    function ResultsController($location, $routeParams, Results, League, Snackbar, Authentication, Team) {
        var vm = this;

        vm.results = undefined;
        vm.playerFields = undefined;
        vm.teams = undefined;
        vm.result = { 'homeTeam': {}, 'awayTeam': {}, 'outcome': null};
        vm.addResult = addResult;
        vm.homeTeamFields = undefined;
        vm.awayTeamFields = undefined;
        
        activate();
        function activate() {
            if(!Authentication.isAuthenticated()){
                $location.url('/');
                Snackbar.error('You must be logged in to view this page.');
            }

            League.listPlayerFields().then(playerSuccess, playerError);
            League.listTeamFields().then(teamSuccess, teamError);
            Team.list().then(teamsSuccess, teamsError);
            
            function playerSuccess(data, status, headers, config) {
                vm.playerFields = data.data;
            }
            function playerError(data, status, headers, config) {
                Snackbar.error('Error getting player fields.');
            }
            function teamSuccess(data, status, headers, config) {
                vm.homeTeamFields = data.data;
                vm.awayTeamFields = JSON.parse(JSON.stringify(data.data));
            }
            function teamError (data, status, headers, config) {
                Snackbar.error('Error getting team fields.');
            }
            function teamsSuccess(data, status, headers, config) {
                vm.teams = data.data;
                if(vm.teams.length === 0){
                    $location.url('/teams');
                    Snackbar.error('You must make a team before reporting a match.');
                }
            }
            function teamsError(data, status, headers, config) {
                $location.url('/teams');
                Snackbar.error('You must make a team before reporting a match.');
            }            
        }

        function addResult() {
            if(vm.result.homeTeam.name === vm.result.awayTeam.name) {
                Snackbar.error('Home and Away teams must be different!');
                return;
            }

            vm.result.reporter = Authentication.getAuthenticatedAccount().username;
            Results.add(vm.result).then(resultSuccess, resultError);

            function addTeamStats() {
                for(var i = 0; i < vm.homeTeamFields.length; i++){
                    var stat = vm.homeTeamFields[i];
                    stat.team = vm.result.homeTeam;
                    stat.result = vm.result;
                    Results.addTeamData(stat);
                }       
                for(var i = 0; i < vm.awayTeamFields.length; i++){
                    var stat = vm.awayTeamFields[i];
                    stat.team = vm.result.awayTeam;
                    stat.result = vm.result;
                    Results.addTeamData(stat);                    
                }
            }
            
            function resultSuccess(data, status, headers, config) {
                vm.result.id = data.data;
                addTeamStats();
                $location.url('/results');
                Snackbar.show('Match result added!');
            }
            function resultError(data, status, headers, config) {
                Snackbar.error('Unable to add match result');
            }
        }
    }
})();
