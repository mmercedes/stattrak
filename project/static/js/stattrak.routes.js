(function () {
    'use strict';

    angular
        .module('stattrak.routes')
        .config(config);

    config.$inject = ['$routeProvider'];

    function config($routeProvider) {
        var userRoute = {
            controller: 'ProfileListController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/profile-list.html'
        }
        $routeProvider.when('/register', {
            controller: 'RegisterController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/register.html'
        }).when('/login', {
            controller: 'LoginController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/login.html'
        }).when('/standings', userRoute)
          .when('/league', {
            controller: 'LeagueController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/league.html'
        }).when('/:username', {
            controller: 'ProfileController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/profile.html'
        }).when('/:username/settings', {
            controller: 'ProfileSettingsController',
            controllerAs: 'vm',
            templateUrl: '/static/templates/profile-settings.html'
        }).otherwise('/standings', userRoute);
    }
})();
