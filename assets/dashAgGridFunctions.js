var dagfuncs = (window.dashAgGridFunctions = window.dashAgGridFunctions || {});


// Using Intl.NumberFormat
dagfuncs.Intl = Intl;

dagfuncs.EUR = function (number) {
    return Intl.NumberFormat("de-DE", {
        style: "currency",
        currency: "EUR",
    }).format(number);
};

dagfuncs.JPY = function (number) {
    return Intl.NumberFormat("ja-JP", {
        style: "currency",
        currency: "JPY",
    }).format(number);
};

dagfuncs.USD = function (number) {
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(number);
};

dagfuncs.CAD = function (number) {
    return Intl.NumberFormat("en-CA", {
        style: "currency",
        currency: "CAD",
        currencyDisplay: "code",
    }).format(number);
};

//  Custom Function for blank when NaN
dagfuncs.PercentageFilna = function (number, filna = "") {
    if (isNaN(number)) {
        return filna;
    }
    return Intl.NumberFormat("en-US", {style: "percent"}).format(number);
};

dagfuncs.MoneyFilna = function (number, filna = "") {
    if (isNaN(number)) {
        return filna;
    }
    return Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
    }).format(number);
};

dagfuncs.customCellRendererSelector = (params) => {
    const moodDetails = {
        component: dagcomponentfuncs.MoodRenderer,
    };

    const genderDetails = {
        component: dagcomponentfuncs.GenderRenderer,
        params: {color: '#66c2a5'},
    };

    if (params.data) {
        if (params.data.type  === 'gender') return genderDetails;
        else if (params.data.Country === 'US') return moodDetails;
    }
    return undefined;
};

// https://dash.plotly.com/dash-ag-grid/enterprise-aggregation-custom-functions
// Aggregation with Custom Functions
dagfuncs.ratioValueGetter = function (params) {
    if (!(params.node && params.node.group)) {
      // no need to handle group levels - calculated in the 'ratioAggFunc'      
      return createValueObject(params.data.Sales, params.data.Units);
    }
  }
  dagfuncs.ratioAggFunc = function (params) {
    let goldSum = 0;
    let silverSum = 0;
    params.values.forEach((value) => {
      if (value && value.Sales) {
        goldSum += value.Sales;
      }
      if (value && value.Unit) {
        silverSum += value.Unit;
      }
    });
    return createValueObject(goldSum, silverSum);
  }
  
  function createValueObject(gold, silver) {
    // console.log(gold, silver)
    return {
      gold: gold,
      silver: silver,
      toString: () => `${gold && silver ? gold / silver : 0}`,
    };
  }
  
  dagfuncs.ratioFormatter = function (params) {
    if (!params.value || params.value === 0) return '';
    return '' + Math.round(params.value * 100) / 100;
  }