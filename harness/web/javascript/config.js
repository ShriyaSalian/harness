/*
The following config which disables sce should be disabled once the project is live.
This is because our html are not yet hosted on the server and must be interpolated.
Once the project is live, the includes should be finding the proper paths through
the tomcat service.
*/
GhcnApp.config(function($sceProvider) {
  $sceProvider.enabled(false);
});

/*
The following configurations deal with overriding default behaviors in
angularStrap services.
*/
GhcnApp.config(function($dropdownProvider) {
  angular.extend($dropdownProvider.defaults, {
    container: 'body'
  });
})
