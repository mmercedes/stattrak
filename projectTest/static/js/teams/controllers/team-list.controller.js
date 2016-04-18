(function () {
    'use strict';

    angular
        .module('stattrak.teams.controllers')
        .controller('TeamListController', TeamListController);

    TeamListController.$inject = ['$location', '$routeParams', '$uibModal', 'Team', 'Authentication', 'Snackbar', 'League', 'Profile'];

    function TeamListController($location, $routeParams, $uibModal, Team, Authentication, Snackbar, League, Profile) {
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
            $uibModal.open({
                templateUrl: 'static/templates/register-team.html',
                backdrop: true,
                windowClass: 'modal',
                controller: function ($scope, $uibModalInstance, team, league, log, profiles) {
                    var vm = this;
                    vm.team = { 'name': '', 'players':[]};
                    
                    for(var i = 0; i < league.teamSize; i++){
                        vm.team.players.push({'username':''});
                    }
                    
                    profiles.list().then(profileSuccess, profileError);

                    function profileSuccess(data, status, headers, config) {
                        vm.players = data.data;
                    }

                    function profileError(data, status, headers, config) {
                        log.error('No users found! Register users before creating teams.');
                        $uibModalInstance.dismiss('cancel');
                    }
                    
                    vm.submit = function () {
                        var players = [];
                        for(var i = 0; i < league.teamSize; i++){
                            var name = vm.team.players[i].username;
                            if(players.indexOf(name) > -1){
                                log.error('All players on a team must be unique!');
                                return;
                            }
                            if(name == '') {
                                log.error('Not enough players to create this team!');
                                return;
                            }
                            players.push(name);
                        }
                        team.create(vm.team).then(teamSuccess, teamError);

                        function teamSuccess(data, status, headers, config) {
                            vm.team = data.data;
                            log.show('Team created!');
                        }
                        function teamError(data, status, headers, config) {
                            log.error('Error creating team!');
                        }
                            
                        $uibModalInstance.dismiss('cancel');
                    }
                    vm.cancel = function () {
                        $uibModalInstance.dismiss('cancel');
                    };
                },
                controllerAs: 'vm',
                resolve: {
                    team: function() {
                        return Team;
                    },
                    league: function() {
                        return vm.league;
                    },
                    log: function() {
                        return Snackbar;
                    },
                    profiles: function() {
                        return Profile;
                    }
                }
            });
        }
    }
})();
