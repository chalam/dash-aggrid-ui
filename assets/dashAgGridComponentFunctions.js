var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.StockLink = function (props) {
    return React.createElement(
        'a',
        {href: 'https://finance.yahoo.com/quote/' + props.value},
        props.value
    );
};

dagcomponentfuncs.MoodRenderer = params => {
    return React.createElement('span', {style: {fontSize: '1.5em'}}, params.value === 'US' ? ' US 😀' : `params.value 😞`)
};

dagcomponentfuncs.GenderRenderer = params => {
    const icon = params.value === 'Male' ? 'fas fa-mars fa-lg' : 'fas fa-venus fa-lg';
    return React.createElement('div', null, [
        React.createElement('i', {className: icon, style: {color: params.color}}),
        ` ${params.value}`
    ])
};