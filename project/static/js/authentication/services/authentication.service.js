(function () {
    'use strict';

    angular
        .module('stattrak.authentication.services')
        .factory('Authentication', Authentication);

    Authentication.$inject = ['$cookies', '$http'];

    function Authentication($cookies, $http) {

        function register(email, password, username) {

            function registerSuccess(data, status, headers, config) {
                Authentication.login(email, password);
            }
            function registerError(data, status, headers, config) {
                console.error('Registration Failed');
            }

            return $http.post('/api/v1/accounts/', {
                username: username,
                password: password,
                email: email
            }).then(registerSuccess, registerError);

        }

        function login(email, password) {
            function loginSuccess(data, status, headers, config) {
                Authentication.setAuthenticatedAccount(data.data);
                window.location = '/';
            }

            function loginError(data, status, headers, config) {
                console.error('Login Failed');
            }
            
            return $http.post('/api/v1/auth/login/', {
                email: email, password: password
            }).then(loginSuccess, loginError);
        }

        function logout() {
            function logoutSuccess(data, status, headers, config) {
                Authentication.unauthenticate();
                window.location = '/';
            }
            function logoutError(data, status, headers, config) {
                console.error('Unable to logout');
            }

            return $http.post('/api/v1/auth/logout/')
                .then(logoutSuccess, logoutError);
        }

        function getAuthenticatedAccount() {
            if (!$cookies.authenticatedAccount) {
                return;
            }
            return JSON.parse($cookies.authenticatedAccount);
        }

        function setAuthenticatedAccount(account) {
            $cookies.authenticatedAccount = JSON.stringify(account);
        }

        function isAuthenticated() {
            return !!$cookies.authenticatedAccount;
        }

        function unauthenticate() {
            delete $cookies.authenticatedAccount;
        }
        
        var Authentication = {
            login: login,
            register: register,
            logout: logout,
            getAuthenticatedAccount: getAuthenticatedAccount,
            setAuthenticatedAccount: setAuthenticatedAccount,
            isAuthenticated: isAuthenticated,
            unauthenticate: unauthenticate
        };

        return Authentication;
    }
})();
