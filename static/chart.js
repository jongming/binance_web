// var chart2 = LightweightCharts.createChart(document.getElementById('chart'), {
// 	width: 600,
//   height: 300,
// 	layout: {
// 		backgroundColor: '#000000',
// 		textColor: 'rgba(255, 255, 255, 0.9)',
// 	},
// 	grid: {
// 		vertLines: {
// 			color: 'rgba(197, 203, 206, 0.5)',
// 		},
// 		horzLines: {
// 			color: 'rgba(197, 203, 206, 0.5)',
// 		},
// 	},
// 	crosshair: {
// 		mode: LightweightCharts.CrosshairMode.Normal,
// 	},
// 	rightPriceScale: {
// 		borderColor: 'rgba(197, 203, 206, 0.8)',
// 	},
// 	timeScale: {
// 		borderColor: 'rgba(197, 203, 206, 0.8)',
// 	},
// });

function lightweightchart(chartID){
	var _chart = LightweightCharts.createChart(document.getElementById(chartID), {
		width: 600,
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

function smaLine(_chart){
	var _smaLine = _chart.addLineSeries({
		color:'rgba(255,82,82, 0.8)',
		lineWidth:2,
	});
	return _smaLine;
} 

var chart = new lightweightchart('chart1')
var candleSeries = new candles(chart)
var volumeSeries = new volume(chart)
//var smaline = new smaLine(chart)

var chart2 = new lightweightchart('chart2')
var candleSeries2 = new candles(chart2)
var volumeSeries2 = new volume(chart2)
//var smaline2 = new smaLine(chart2)

var chart3 = new lightweightchart('chart3')
var candleSeries3 = new candles(chart3)
var volumeSeries3 = new volume(chart3)
//var smaline2 = new smaLine(chart2)


// var candleSeries2 = chart.addCandlestickSeries({
//   upColor: '#00ff00',
//   downColor: '#ff0000',
//   borderDownColor: '#ff0000',
//   borderUpColor: '#00ff00',
//   wickDownColor: '#ff0000',
//   wickUpColor: '#00ff00',
// });



// var volumeSeries = chart.addHistogramSeries({
// 	//color: 'rgba(76, 175, 80, 0.5)',
// 	priceFormat: {
// 		type: 'volume',
// 	},
// 	priceLineVisible: false,
// 	overlay: true,
// 	scaleMargins: {
// 		top: 0.85,
// 		bottom: 0,
// 	},
// });

function calculateSMA(data, count){
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

 

// candleSeries.setData(
// 	[
// 		{
// 		  "close": 1026.9599609375, 
// 		  "high": 1080.9300537109375, 
// 		  "low": 1010.0, 
// 		  "open": 1080.3699951171875, 
// 		  "time": "2022-01-07"
// 		}, 
// 		{
// 		  "close": 1058.1199951171875, 
// 		  "high": 1059.0999755859375, 
// 		  "low": 980.0, 
// 		  "open": 1000.0, 
// 		  "time": "2022-01-10"
// 		}, 
// 		{
// 		  "close": 1064.4000244140625, 
// 		  "high": 1075.8499755859375, 
// 		  "low": 1038.8199462890625, 
// 		  "open": 1053.6700439453125, 
// 		  "time": "2022-01-11"
// 		}, 
// 		{
// 		  "close": 1106.219970703125, 
// 		  "high": 1114.8399658203125, 
// 		  "low": 1072.5899658203125, 
// 		  "open": 1078.8499755859375, 
// 		  "time": "2022-01-12"
// 		}, 
// 		{
// 		  "close": 1031.56005859375, 
// 		  "high": 1115.5999755859375, 
// 		  "low": 1026.5400390625, 
// 		  "open": 1109.0699462890625, 
// 		  "time": "2022-01-13"
// 		}, 
// 		{
// 		  "close": 1049.6099853515625, 
// 		  "high": 1052.0, 
// 		  "low": 1013.3800048828125, 
// 		  "open": 1019.8800048828125, 
// 		  "time": "2022-01-14"
// 		}, 
// 		{
// 		  "close": 1030.510009765625, 
// 		  "high": 1070.7900390625, 
// 		  "low": 1016.0599975585938, 
// 		  "open": 1026.6099853515625, 
// 		  "time": "2022-01-18"
// 		}, 
// 		{
// 		  "close": 995.6500244140625, 
// 		  "high": 1054.6700439453125, 
// 		  "low": 995.0, 
// 		  "open": 1041.7099609375, 
// 		  "time": "2022-01-19"
// 		}, 
// 		{
// 		  "close": 996.27001953125, 
// 		  "high": 1041.6600341796875, 
// 		  "low": 994.0, 
// 		  "open": 1009.72998046875, 
// 		  "time": "2022-01-20"
// 		}, 
// 		{
// 		  "close": 943.9000244140625, 
// 		  "high": 1004.5499877929688, 
// 		  "low": 940.5, 
// 		  "open": 996.3400268554688, 
// 		  "time": "2022-01-21"
// 		}, 
// 		{
// 		  "close": 930.0, 
// 		  "high": 933.510009765625, 
// 		  "low": 851.469970703125, 
// 		  "open": 904.760009765625, 
// 		  "time": "2022-01-24"
// 		}, 
// 		{
// 		  "close": 918.4000244140625, 
// 		  "high": 951.260009765625, 
// 		  "low": 903.2100219726562, 
// 		  "open": 914.2000122070312, 
// 		  "time": "2022-01-25"
// 		}, 
// 		{
// 		  "close": 937.4099731445312, 
// 		  "high": 987.6900024414062, 
// 		  "low": 906.0, 
// 		  "open": 952.4299926757812, 
// 		  "time": "2022-01-26"
// 		}, 
// 		{
// 		  "close": 829.0999755859375, 
// 		  "high": 935.3900146484375, 
// 		  "low": 829.0, 
// 		  "open": 933.3599853515625, 
// 		  "time": "2022-01-27"
// 		}, 
// 		{
// 		  "close": 846.3499755859375, 
// 		  "high": 857.5, 
// 		  "low": 792.010009765625, 
// 		  "open": 831.5599975585938, 
// 		  "time": "2022-01-28"
// 		}, 
// 		{
// 		  "close": 936.719970703125, 
// 		  "high": 937.989990234375, 
// 		  "low": 862.0499877929688, 
// 		  "open": 872.7100219726562, 
// 		  "time": "2022-01-31"
// 		}, 
// 		{
// 		  "close": 931.25, 
// 		  "high": 943.7000122070312, 
// 		  "low": 905.0, 
// 		  "open": 935.2100219726562, 
// 		  "time": "2022-02-01"
// 		}, 
// 		{
// 		  "close": 905.6599731445312, 
// 		  "high": 931.5, 
// 		  "low": 889.4099731445312, 
// 		  "open": 928.1799926757812, 
// 		  "time": "2022-02-02"
// 		}, 
// 		{
// 		  "close": 891.1400146484375, 
// 		  "high": 937.0, 
// 		  "low": 880.52001953125, 
// 		  "open": 882.0, 
// 		  "time": "2022-02-03"
// 		}, 
// 		{
// 		  "close": 923.3200073242188, 
// 		  "high": 936.5, 
// 		  "low": 881.1699829101562, 
// 		  "open": 897.219970703125, 
// 		  "time": "2022-02-04"
// 		}, 
// 		{
// 		  "close": 907.3400268554688, 
// 		  "high": 947.77001953125, 
// 		  "low": 902.7100219726562, 
// 		  "open": 923.7899780273438, 
// 		  "time": "2022-02-07"
// 		}, 
// 		{
// 		  "close": 922.0, 
// 		  "high": 926.2899780273438, 
// 		  "low": 894.7999877929688, 
// 		  "open": 905.530029296875, 
// 		  "time": "2022-02-08"
// 		}, 
// 		{
// 		  "close": 932.0, 
// 		  "high": 946.27001953125, 
// 		  "low": 920.0, 
// 		  "open": 935.0, 
// 		  "time": "2022-02-09"
// 		}, 
// 		{
// 		  "close": 904.5499877929688, 
// 		  "high": 943.8099975585938, 
// 		  "low": 896.7000122070312, 
// 		  "open": 908.3699951171875, 
// 		  "time": "2022-02-10"
// 		}, 
// 		{
// 		  "close": 860.0, 
// 		  "high": 915.9600219726562, 
// 		  "low": 850.7000122070312, 
// 		  "open": 909.6300048828125, 
// 		  "time": "2022-02-11"
// 		}, 
// 		{
// 		  "close": 875.760009765625, 
// 		  "high": 898.8800048828125, 
// 		  "low": 853.1500244140625, 
// 		  "open": 861.5700073242188, 
// 		  "time": "2022-02-14"
// 		}, 
// 		{
// 		  "close": 922.4299926757812, 
// 		  "high": 923.0, 
// 		  "low": 893.3800048828125, 
// 		  "open": 900.0, 
// 		  "time": "2022-02-15"
// 		}, 
// 		{
// 		  "close": 923.3900146484375, 
// 		  "high": 926.4299926757812, 
// 		  "low": 901.2100219726562, 
// 		  "open": 914.0499877929688, 
// 		  "time": "2022-02-16"
// 		}, 
// 		{
// 		  "close": 876.3499755859375, 
// 		  "high": 918.5, 
// 		  "low": 874.0999755859375, 
// 		  "open": 913.260009765625, 
// 		  "time": "2022-02-17"
// 		}, 
// 		{
// 		  "close": 856.97998046875, 
// 		  "high": 886.8699951171875, 
// 		  "low": 837.6099853515625, 
// 		  "open": 886.0, 
// 		  "time": "2022-02-18"
// 		}, 
// 		{
// 		  "close": 821.530029296875, 
// 		  "high": 856.72998046875, 
// 		  "low": 801.0999755859375, 
// 		  "open": 834.1300048828125, 
// 		  "time": "2022-02-22"
// 		}, 
// 		{
// 		  "close": 764.0399780273438, 
// 		  "high": 835.2999877929688, 
// 		  "low": 760.5599975585938, 
// 		  "open": 830.4299926757812, 
// 		  "time": "2022-02-23"
// 		}, 
// 		{
// 		  "close": 800.77001953125, 
// 		  "high": 802.47998046875, 
// 		  "low": 700.0, 
// 		  "open": 700.3900146484375, 
// 		  "time": "2022-02-24"
// 		}, 
// 		{
// 		  "close": 809.8699951171875, 
// 		  "high": 819.5, 
// 		  "low": 782.4000244140625, 
// 		  "open": 809.22998046875, 
// 		  "time": "2022-02-25"
// 		}, 
// 		{
// 		  "close": 870.4299926757812, 
// 		  "high": 876.8599853515625, 
// 		  "low": 814.7100219726562, 
// 		  "open": 815.010009765625, 
// 		  "time": "2022-02-28"
// 		}, 
// 		{
// 		  "close": 864.3699951171875, 
// 		  "high": 889.8800048828125, 
// 		  "low": 853.780029296875, 
// 		  "open": 869.6799926757812, 
// 		  "time": "2022-03-01"
// 		}, 
// 		{
// 		  "close": 879.8900146484375, 
// 		  "high": 886.47998046875, 
// 		  "low": 844.27001953125, 
// 		  "open": 872.1300048828125, 
// 		  "time": "2022-03-02"
// 		}, 
// 		{
// 		  "close": 839.2899780273438, 
// 		  "high": 886.4400024414062, 
// 		  "low": 832.5999755859375, 
// 		  "open": 878.77001953125, 
// 		  "time": "2022-03-03"
// 		}, 
// 		{
// 		  "close": 838.2899780273438, 
// 		  "high": 855.6500244140625, 
// 		  "low": 825.1599731445312, 
// 		  "open": 849.0999755859375, 
// 		  "time": "2022-03-04"
// 		}, 
// 		{
// 		  "close": 804.5800170898438, 
// 		  "high": 866.1400146484375, 
// 		  "low": 804.5700073242188, 
// 		  "open": 856.2999877929688, 
// 		  "time": "2022-03-07"
// 		}, 
// 		{
// 		  "close": 824.4000244140625, 
// 		  "high": 849.989990234375, 
// 		  "low": 782.1699829101562, 
// 		  "open": 795.530029296875, 
// 		  "time": "2022-03-08"
// 		}, 
// 		{
// 		  "close": 858.969970703125, 
// 		  "high": 860.5599975585938, 
// 		  "low": 832.010009765625, 
// 		  "open": 839.47998046875, 
// 		  "time": "2022-03-09"
// 		}, 
// 		{
// 		  "close": 838.2999877929688, 
// 		  "high": 854.4500122070312, 
// 		  "low": 810.3599853515625, 
// 		  "open": 851.4500122070312, 
// 		  "time": "2022-03-10"
// 		}, 
// 		{
// 		  "close": 795.3499755859375, 
// 		  "high": 843.7999877929688, 
// 		  "low": 793.77001953125, 
// 		  "open": 840.2000122070312, 
// 		  "time": "2022-03-11"
// 		}, 
// 		{
// 		  "close": 766.3699951171875, 
// 		  "high": 800.7000122070312, 
// 		  "low": 756.0399780273438, 
// 		  "open": 780.6099853515625, 
// 		  "time": "2022-03-14"
// 		}, 
// 		{
// 		  "close": 801.8900146484375, 
// 		  "high": 805.5700073242188, 
// 		  "low": 756.5700073242188, 
// 		  "open": 775.27001953125, 
// 		  "time": "2022-03-15"
// 		}, 
// 		{
// 		  "close": 840.22998046875, 
// 		  "high": 842.0, 
// 		  "low": 802.260009765625, 
// 		  "open": 809.0, 
// 		  "time": "2022-03-16"
// 		}, 
// 		{
// 		  "close": 871.5999755859375, 
// 		  "high": 875.0, 
// 		  "low": 825.7177734375, 
// 		  "open": 830.989990234375, 
// 		  "time": "2022-03-17"
// 		}, 
// 		{
// 		  "close": 905.3900146484375, 
// 		  "high": 907.8499755859375, 
// 		  "low": 867.4000244140625, 
// 		  "open": 874.489990234375, 
// 		  "time": "2022-03-18"
// 		}, 
// 		{
// 		  "close": 921.1599731445312, 
// 		  "high": 942.8499755859375, 
// 		  "low": 907.0900268554688, 
// 		  "open": 914.97998046875, 
// 		  "time": "2022-03-21"
// 		}, 
// 		{
// 		  "close": 993.97998046875, 
// 		  "high": 997.8599853515625, 
// 		  "low": 921.75, 
// 		  "open": 930.0, 
// 		  "time": "2022-03-22"
// 		}, 
// 		{
// 		  "close": 999.1099853515625, 
// 		  "high": 1040.699951171875, 
// 		  "low": 976.4000244140625, 
// 		  "open": 979.9400024414062, 
// 		  "time": "2022-03-23"
// 		}, 
// 		{
// 		  "close": 1013.9199829101562, 
// 		  "high": 1024.489990234375, 
// 		  "low": 988.7999877929688, 
// 		  "open": 1009.72998046875, 
// 		  "time": "2022-03-24"
// 		}, 
// 		{
// 		  "close": 1010.6400146484375, 
// 		  "high": 1021.7999877929688, 
// 		  "low": 997.3200073242188, 
// 		  "open": 1008.0, 
// 		  "time": "2022-03-25"
// 		}, 
// 		{
// 		  "close": 1091.8399658203125, 
// 		  "high": 1097.8800048828125, 
// 		  "low": 1053.5999755859375, 
// 		  "open": 1065.0999755859375, 
// 		  "time": "2022-03-28"
// 		}, 
// 		{
// 		  "close": 1099.5699462890625, 
// 		  "high": 1114.77001953125, 
// 		  "low": 1073.1099853515625, 
// 		  "open": 1107.989990234375, 
// 		  "time": "2022-03-29"
// 		}, 
// 		{
// 		  "close": 1093.989990234375, 
// 		  "high": 1113.8800048828125, 
// 		  "low": 1084.0, 
// 		  "open": 1091.1700439453125, 
// 		  "time": "2022-03-30"
// 		}, 
// 		{
// 		  "close": 1077.5999755859375, 
// 		  "high": 1103.139892578125, 
// 		  "low": 1076.6409912109375, 
// 		  "open": 1094.5699462890625, 
// 		  "time": "2022-03-31"
// 		}, 
// 		{
// 		  "close": 1084.5899658203125, 
// 		  "high": 1094.75, 
// 		  "low": 1066.6400146484375, 
// 		  "open": 1081.1500244140625, 
// 		  "time": "2022-04-01"
// 		}
// ]);

// volumeSeries.setData([
// 	{ time: '2022-01-06', value: 12371207.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-01-07', value: 14891287.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-01-08', value: 12482392.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-01-09', value: 17365762.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-01-12', value: 13236769.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-01-13', value: 13047907.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-01-14', value: 18288710.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-01-18', value: 19470986.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-01-19', value: 18405731.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-01-20', value: 22028957.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-01-21', value: 18482233.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-01-24', value: 7009050.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-01-25', value: 7009050.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-01-26', value: 12308876.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-01-27', value: 14118867.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-01-28', value: 18662989.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-01-31', value: 31142818.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-02-02', value: 27795428.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-03', value: 27795428.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-04', value: 21727411.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-07', value: 26880429.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-08', value: 16948126.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-09', value: 18892182.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-10', value: 16603356.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-02-11', value: 14991438.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-02-14', value: 18892182.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-15', value: 15454706.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-16', value: 13960870.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-17', value: 18902523.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-18', value: 18895777.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-22', value: 20968473.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-02-23', value: 26897008.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-24', value: 55413082.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-25', value: 15077207.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-02-28', value: 14771641.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-02-31', value: 15331758.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-01', value: 13969691.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-03-02', value: 13969691.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-03-03', value: 19245411.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-04', value: 17035848.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-07', value: 16348982.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-08', value: 21425008.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-09', value: 18136000.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-03-10', value: 14259910.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-11', value: 15801548.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-14', value: 11342293.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-15', value: 10074386.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-16', value: 13411691.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-03-17', value: 15223854.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-03-18', value: 16802516.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-21', value: 16802516.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-22', value: 18284771.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-03-23', value: 15109007.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-24', value: 12494109.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-03-25', value: 17806822.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-03-28', value: 25955718.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-03-29', value: 33789235.00, color: 'rgba(255,82,82, 0.8)' },
// 	{ time: '2022-03-30', value: 27260036.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-03-31', value: 28585447.00, color: 'rgba(0, 150, 136, 0.8)' },
// 	{ time: '2022-04-01', value: 13778392.00, color: 'rgba(255,82,82, 0.8)' }
// ]);


fetch('http://localhost:5000/history')
	.then((r) => r.json())
	.then((response) => {
		//console.log(response.stock1.candlesticks)
		document.getElementById('chart1_title').innerHTML = response.stock1.ticker;
		candleSeries.setData(response.stock1.candlesticks);
		volumeSeries.setData(response.stock1.volume);

		document.getElementById('chart2_title').innerHTML = response.stock2.ticker;
		candleSeries2.setData(response.stock2.candlesticks);
		volumeSeries2.setData(response.stock2.volume);

		document.getElementById('chart3_title').innerHTML = response.stock3.ticker;
		candleSeries3.setData(response.stock3.candlesticks);
		volumeSeries3.setData(response.stock3.volume);

		//var smaData = calculateSMA(response.stock1.candlesticks, 8);

		//smaline.setData(smaData);
		//smaline2.setData(smaData);
 	})	
