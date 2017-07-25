/**
 * Created by Tom.Ridd on 08/05/2017.
 */

function filterData(data, filter) {

    var indexFilter = textFilterToIndexFilter(data, filter);
    return applyFilter(data, indexFilter);
}

function numerateColumns(data, columns) {
    _.forEach(columns, function (column) {
        numerateColumn(data, column);
    });
}

function numerateColumn(data, column) {
    var index = data[0].indexOf(column);
    for(row = 1; row < data.length; row++) {
        row[index] = row[index].toFloat();
    }
}

function textFilterToIndexFilter(data, textFilter) {
    var indexFilter = {};
    var headers = data[0];

    for(var key in textFilter) {
        var i = headers.indexOf(key);
        indexFilter[i] = textFilter[key];
    }

    return indexFilter;
}

function applyFilter(data, indexFilter){
    var data2 = _.clone(data);

    var headerRow = data2.shift();
    var filteredRows = [];

    for(var d in data2) {
        var datum = data2[d];
        if(itemPassesFilter(datum, indexFilter)) {
            filteredRows.push(datum);
        }
    }

    filteredRows.unshift(headerRow);
    return filteredRows;
}

function itemPassesFilter(item, filter) {
    if(item[0] === '') { return false; }

    for(var index in filter) {
        if (item[index] !== filter[index]) {
            return false;
        }
    }
    return true;
}

function formatNumber(numStr) {
    var number = numStr.replaceAll("%","");
    var formatted = (number * 1).toLocaleString("en-uk");
    if(formatted === "NaN") {
        return number;
    } else {
        return formatted;
    }
}

function formatNumberWithDecimalPlaces(value, dp) {

    var number = ""+value;
    try {
        number = number.replace("%","");
    } finally {
        var formatted = (number * 1).toLocaleString("en-uk", {minimumFractionDigits: dp, maximumFractionDigits: dp});
        if (formatted !== "NaN") {
            return formatted;
        }
    }
    return number;
}

function seriesDecimalPlaces(series) {
    var maxDp = 0;
    for(var s in series) {
        var dp = decimalPlaces(series[s]);
        if (dp > maxDp) {
            maxDp = dp;
        }
    }
    return maxDp;
}

function seriesCouldBeYear(series) {
    for(var s in series) {
        var val = series[s];
        if(decimalPlaces(val) > 0 || val < 1950 || val > 2050) {
            return false;
        }
    }
    return true;
}

function decimalPlaces(valueStr) {
    if(valueStr) {
        var numStr = valueStr.toString().replace("%","");
        var pieces = numStr.split(".");
        if (pieces.length < 2) {
            return 0;
        } else {
            return pieces[1].length;
        }
    } else {
        return 0;
    }
}

function uniqueDataInColumn(data, index) {
    var values = _.map(data.slice(start = 0), function(item) {
        return item[index]; });
    return _.uniq(values).sort();
}

function uniqueDataInColumnOrdered(data, index, order_column) {
    // Sort by the specified column
    var sorted = _.sortBy(data, function (item) {
        return item[order_column];
    });
    // Pull out unique items
    var values = _.map(sorted, function(item) { return item[index];});
    return _.uniq(values);
}

function uniqueDataInColumnMaintainOrder(data, index) {
    var values = [];
    var used = {};
    _.forEach(data, function (item) {
        if(!(item[index] in used)) {
            values.push(item[index]);
            used[item[index]] = 1;
        }
    });
    return values;
}

// If we running under Node - required for testing
if(typeof exports !== 'undefined') {
    var _ = require('../vendor/underscore-min');

    exports.decimalPlaces = decimalPlaces;
    exports.seriesDecimalPlaces = seriesDecimalPlaces;
    exports.seriesCouldBeYear = seriesCouldBeYear;
    exports.formatNumberWithDecimalPlaces = formatNumberWithDecimalPlaces;

    exports.uniqueDataInColumn = uniqueDataInColumn;
    exports.uniqueDataInColumnOrdered = uniqueDataInColumnOrdered;
    exports.uniqueDataInColumnMaintainOrder = uniqueDataInColumnMaintainOrder;

}