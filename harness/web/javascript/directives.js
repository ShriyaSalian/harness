GhcnApp.directive('hnStructureTree', ['$tooltip', '$compile',

    function($tooltip, $compile) {
        var link = function($scope, $el, $attrs) {
            var canvas = d3.select($el[0]).append("svg").attr("class", "overlay");
            var group = canvas.append("g");
            canvas.call(callbacks['zoom_listener']);
            var update = 'test';
        }
}]);


GhcnApp.directive( 'elemReady', function( $parse ) {
   return {
       restrict: 'A',
       link: function( $scope, elem, attrs ) {
          elem.ready(function(){
            $scope.$apply(function(){
                var func = $parse(attrs.elemReady);
                func($scope);
            })
          })
       }
    }
});
