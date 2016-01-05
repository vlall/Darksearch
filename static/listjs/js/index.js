/*
    * LOVELY THINGS
    */

var options = {
  valueNames: [ 'name', 'description', 'category' ]
};

var featureList = new List('lovely-things-list', options);

$('#filter-social-media').click(function() {
  featureList.filter(function(item) {
    if (item.values().category == "Social Media") {
      return true;
    } else {
      return false;
    }
  });
  return false;
});

$('#filter-dark-web').click(function() {
  featureList.filter(function(item) {
    if (item.values().category == "Dark Web") {
      return true;
    } else {
      return false;
    }
  });
  return false;
});
$('#filter-none').click(function() {
  featureList.filter();
  return false;
});