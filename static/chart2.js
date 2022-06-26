
function lightweightchart(chartID){
	var _chart = LightweightCharts.createChart(document.getElementById(chartID), {
		width: 500,
	  height: 300,
		layout: {
			backgroundColor: '#000000',
			textColor: 'rgba(255, 255, 255, 0.9)',
		},
		grid: {
			vertLines: {
				color: 'rgba(197, 203, 206, 0.5)',
			},
			horzLines: {
				color: 'rgba(197, 203, 206, 0.5)',
			},
		},
		crosshair: {
			mode: LightweightCharts.CrosshairMode.Normal,
		},
		rightPriceScale: {
			borderColor: 'rgba(197, 203, 206, 0.8)',
		},
		timeScale: {
			borderColor: 'rgba(197, 203, 206, 0.8)',
		},
	});
	return _chart;
}

function candles(_chart){
	var _candleSeries = _chart.addCandlestickSeries({
		upColor: '#00ff00',
		downColor: '#ff0000',
		borderDownColor: '#ff0000',
		borderUpColor: '#00ff00',
		wickDownColor: '#ff0000',
		wickUpColor: '#00ff00',
	  });
	return _candleSeries;
}

function volume(_chart){
	var _volumeSeries = _chart.addHistogramSeries({
		color: '#26a69a',
		priceFormat: {
			type: 'volume',
		},
		priceScaleId: '',
		scaleMargins: {
			top: 0.8,
			bottom: 0,
		},
	});
	return _volumeSeries
}

function smaLine(_chart, count){
	var _color = 'rgba(255,215,0, 0.8)';
	var _lineWidth = 2;

	if (count == 21){
		_color = 'rgba(138,43,226, 0.8)';
		_lineWidth = 3;
	}else if (count == 50) {
		_color = 'rgba(255,82,82, 0.8)';
		_lineWidth = 3;
	}

	var _smaLine = _chart.addLineSeries({
		color: _color,
		lineWidth: _lineWidth,
	});
	return _smaLine;
} 

function hLine(_chart){
	var _hLine = _chart.addLineSeries({
		color:'rgba(255,255,255, 0.8)',
		lineWidth:5,
	});
	return _hLine;
}

function calculateHline(data, count, value){
	var avg = function(data) {
		var sum = 0;
		for (var i = 0; i < data.length; i++) {
		   sum += data[i].close;
		}
		return sum / data.length;
	  };
	  var result = [];
	for (var i=count - 1, len=data.length; i < len; i++){
		var val = avg(data.slice(i - count + 1, i));
		result.push({ time: data[i].time, value: value});
	  }
	// console.log(result)
	return result;
}

function calculateSMA(data, count){
	console.log("calculateSMA:"+count)
	var avg = function(data) {
	  var sum = 0;
	  for (var i = 0; i < data.length; i++) {
		 sum += data[i].close;
	  }
	  return sum / data.length;
	};
	var result = [];
	for (var i=count - 1, len=data.length; i < len; i++){
	  var val = avg(data.slice(i - count + 1, i));
	  result.push({ time: data[i].time, value: val});
	}
	return result;
}

//populate data in elements
if (typeof stocks_data !== 'undefined'){
	// for (i=1; i<Object.keys(stocks_data).length+1; i++){
	for (i=0; i<Object.keys(stocks_data).length; i++){	
		window['chart'+i] = new lightweightchart('chart'+i)

		window['candleSeries'+i] = new candles(window['chart'+i])
		window['candleSeries'+i].setData(eval('stocks_data.stock'+i+'.candlesticks'));

		window['volumeSeries'+i] = new volume(window['chart'+i])
		window['volumeSeries'+i].setData(eval('stocks_data.stock'+i+'.volume'));

		window['smaData8'+i] = calculateSMA(eval('stocks_data.stock'+i+'.candlesticks'), 8);
		window['smaData21'+i] = calculateSMA(eval('stocks_data.stock'+i+'.candlesticks'), 21);
		window['smaData50'+i] = calculateSMA(eval('stocks_data.stock'+i+'.candlesticks'), 50);
		
		window['smaline8'+i] = new smaLine(window['chart'+i], 8)
		window['smaline8'+i].setData(window['smaData8'+i]);

		window['smaline21'+i] = new smaLine(window['chart'+i], 21)
		window['smaline21'+i].setData(window['smaData21'+i]);

		window['smaline50'+i] = new smaLine(window['chart'+i], 50)
		window['smaline50'+i].setData(window['smaData50'+i]);

		// window['hLine'+i] = new hLine(window['chart'+i])
		// window['hData'+i] = calculateHline(eval('stocks_data.stock'+i+'.candlesticks'), 8, 360);
		// window['hLine'+i].setData(window['hData'+i]);
	}
}

//populate data in elements
if (typeof rs_data !== 'undefined'){
	// for (i=1; i<Object.keys(rs_data).length+1; i++){
	for (i=0; i<Object.keys(rs_data).length; i++){
		// window['chart'+i] = new lightweightchart('chart'+i)
		// window['candleSeries'+i] = new candles(window['chart'+i])
		// window['volumeSeries'+i] = new volume(window['chart'+i])
		// window['smaData'+i] = calculateSMA(eval('stocks_data.stock'+i+'.candlesticks'), 8);
		// window['smaline'+i] = new smaLine(window['chart'+i])
		document.getElementById('chart'+i+'_title').innerHTML = eval('stocks_data.stock'+i+'.ticker');
		document.getElementById('chart'+i+'_sector').innerHTML = eval('rs_data.stock'+i+'.sector');
		document.getElementById('chart'+i+'_iindustry').innerHTML = eval('rs_data.stock'+i+'.iindustry');
		document.getElementById('chart'+i+'_findustry').innerHTML = eval('rs_data.stock'+i+'.findustry');
		// window['candleSeries'+i].setData(eval('stocks_data.stock'+i+'.candlesticks'));
		// window['volumeSeries'+i].setData(eval('stocks_data.stock'+i+'.volume'));
		// window['smaline'+i].setData(window['smaData'+i]);

	}
}
