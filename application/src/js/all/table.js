

if ('addEventListener' in document &&
    document.querySelectorAll
  ) {

  document.addEventListener('DOMContentLoaded', function() {

    var tables = document.querySelectorAll('[data-module*="eff-sortable-headers"]')

    for (var i = tables.length - 1; i >= 0; i--) {

      var table = tables[i]

      new SortableTable(table, {})
    };

  })

}
