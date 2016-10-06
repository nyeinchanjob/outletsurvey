var MyApp = angular.module('MyApp', ['ngMaterial', 'ngMessages']);
MyApp.controller('AppCtrl', ['$scope', '$mdDialog', '$mdSidenav',  function($scope, $mdDialog, $mdSidenav) {
    $scope.show_brand_detail = false;
    $scope.toggleLeft = buildToggler('left');
    function buildToggler(navID) {
      return function() {
        // Component lookup should always be available since we are not using `ng-if`
        $mdSidenav(navID).toggle();
      }
  };

    $scope.isOpenLeft = function(){
      return true;//$mdSidenav('left').isOpen();
    };

    $scope.brand_detail_show = false;
    $scope.show_brand_detail = function() {
        $scope.brand_detail_show = true;
    }

    $scope.hide_brand_detail = function() {
        $scope.brand_detail_show = false;
    }
}]);
