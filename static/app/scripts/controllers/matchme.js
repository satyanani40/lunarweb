'use strict';

/**
 * @ngdoc function
 * @name weberApp.controller:MatchMeCtrl
 * @description
 * # MatchMeCtrl
 * Controller of the weberApp
 */
angular.module('weberApp')
	.controller('MatchMeCtrl', function($scope, $auth, Restangular, InfinitePosts, $alert, $http, CurrentUser, UserService) {
		$scope.UserService = UserService;
        alert("hai");
		$http.get('/api/me', {
			headers: {
				'Content-Type': 'application/json'
			}
		}).success(function(user_id) {
			Restangular.one('people', JSON.parse(user_id)).get().then(function(user) {
				$scope.user = user;
				$scope.infinitePosts = new InfinitePosts(user);
				if (user.friends.length !== 0) {
					Restangular.all('people').getList().then(function(friends) {
						$scope.friends = friends;
					});
				}
				$scope.submit_post = function() {
					$scope.infinitePosts.addPost($scope.new_post);
					$scope.new_post = '';
				};
			});
		});
	});