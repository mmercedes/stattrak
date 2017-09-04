(function () {
    'use strict';

    angular
        .module('stattrak.results.controllers')
        .controller('ResultsListController', ResultsListController);

    ResultsListController.$inject = ['$location', '$routeParams', 'Results', 'Snackbar', 'Authentication'];

    function ResultsListController($location, $routeParams, Results, Snackbar, Authentication) {
        var vm = this;

        vm.results = undefined;
        vm.reportMatch = reportMatch;
        activate();

        function activate() {
            Results.list().then(resultsSuccess, resultsError);
            
            function resultsSuccess(data, status, headers, config) {
                vm.results = data.data;
            }
            function resultsError(data, status, headers, config) {
                Snackbar.error('Error getting recent matches.');
            }
        }

        function reportMatch() {
            $location.url('/report');
        }
    }
})();
