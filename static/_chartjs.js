class zchartjs {
    constructor(chartID, data){
        this.chartID = chartID;
        this.date = data;

        this.addCandlestickSeries({
            upColor: '#00ff00',
            downColor: '#ff0000',
            borderDownColor: '#ff0000',
            borderUpColor: '#00ff00',
            wickDownColor: '#ff0000',
            wickUpColor: '#00ff00',
          });
    }

    // lightweightchart(chartID){
    //     var _chart = LightweightCharts.createChart(document.getElementById(chartID), {
    //         width: 600,
    //       height: 300,
    //         layout: {
    //             backgroundColor: '#000000',
    //             textColor: 'rgba(255, 255, 255, 0.9)',
    //         },
    //         grid: {
    //             vertLines: {
    //                 color: 'rgba(197, 203, 206, 0.5)',
    //             },
    //             horzLines: {
    //                 color: 'rgba(197, 203, 206, 0.5)',
    //             },
    //         },
    //         crosshair: {
    //             mode: LightweightCharts.CrosshairMode.Normal,
    //         },
    //         rightPriceScale: {
    //             borderColor: 'rgba(197, 203, 206, 0.8)',
    //         },
    //         timeScale: {
    //             borderColor: 'rgba(197, 203, 206, 0.8)',
    //         },
    //     });
    //     return _chart;
    // }

    
}