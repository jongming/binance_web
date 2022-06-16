class Layout_charts_n_data{
    constructor(){

    }

    lightweightchart(index){
        var i = index;
        var _str = '<td class="td_tradingview_chart">'+
                        '<div id="chart'+i+'"></div>'+
                    '</td>' 
        return _str
    }

    stock_info(index, data){
        var i = index;
        var rs_data = data;
        var _ticker = eval('rs_data.stock'+i+'.ticker')
        var _rs_cmp = eval('rs_data.stock'+i+'.cmp')
        var _cmpLast = _rs_cmp[_rs_cmp.length-1]
        var _rs_eps = eval('rs_data.stock'+i+'.eps')
        var _epsLast = _rs_eps[_rs_eps.length-1]
        var _rs_rs = eval('rs_data.stock'+i+'.rs')
        var _rsLast = _rs_rs[_rs_rs.length-1]
        var _rs_smr = eval('rs_data.stock'+i+'.smr')
        var _smrLast = _rs_smr[_rs_smr.length-1]
        var _rs_ad = eval('rs_data.stock'+i+'.ad')
        var _adLast = _rs_ad[_rs_ad.length-1]
        var _fin_dwn = eval('rs_data.stock'+i+'.find_dwn')
        var _str = '<td class="info">'+
                    '<a href="https://www.tradingview.com/chart/7wEqA5CN/?symbol='+_ticker+'" target="_blank">'+
                        '<div class="chart_title_class" id="chart'+i+'_title"></div>'+
                    '</a>'+
                    '<div id="ibd_rating">'+
                        '<b>IBD Rating:</b>'+
                        '<div class="ibd_rating_item">'+
                            '<span>&nbsp;&nbsp;&nbsp;Composit: </span>'+_cmpLast+
                        '</div>'+
                        '<div class="ibd_rating_item">'+
                            '<span>&nbsp;&nbsp;&nbsp;EPS: </span>'+_epsLast+
                        '</div>'+
                        '<div class="ibd_rating_item">'+
                            '<span>&nbsp;&nbsp;&nbsp;RS: </span>'+_rsLast+
                        '</div>'+
                        '<div class="ibd_rating_item">'+
                            '<span>&nbsp;&nbsp;&nbsp;SMR: </span>'+_smrLast+
                        '</div>'+
                        '<div class="ibd_rating_item">'+
                            '<span>&nbsp;&nbsp;&nbsp;A/D: </span>'+_adLast+
                        '</div>'+
                    '</div>'+
                    '<div class="sector">'+
                        '<div><b>Sector: </b><span id="chart'+i+'_sector"></span></div>'+                        
                    '</div>'+
                    '<div class="industry"><b>Industry:</b><br/>'+
                        '&nbsp;&nbsp;&nbsp;(IBD) <span class="industry" id="chart'+i+'_iindustry"></span></br>'+
                        '&nbsp;&nbsp;&nbsp;(Finviz) <span class="industry" id="chart'+i+'_findustry"></span></br>'+
                        '<div>'+
                            '<div>&nbsp;&nbsp;&nbsp;<b>Rank:</b> '+_fin_dwn[0][0]+'/144</div>'+
                            '<div>&nbsp;&nbsp;&nbsp;<b>PerfDay:</b> '+_fin_dwn[0][3]+'</div>'+
                            '<div>&nbsp;&nbsp;&nbsp;<b>PerfWeek:</b> '+_fin_dwn[0][4]+'</div>'+
                            '<div>&nbsp;&nbsp;&nbsp;<b>PerfMonth:</b> '+_fin_dwn[0][5]+'</div>'+
                        '</div>'+
                    '</div>'+
                '</td>'
        return _str
    }

    chartjs(index){ //Chartjs
        var i=index;
        var _str = '<td class="td_chartjs_chart">'+
                        '<div>' +
                        '<canvas id="chjs_chart'+i+'" style="width:100%;max-width:600px; vertical-align:text-top;"></canvas>'+
                        '</div>' +
                    '</td>'
        return _str
    }

    industry_stock_info(i, data){
        var _ind = eval('data.ind'+i+'.industry')
        console.log("_________________")
        var _stock_data = eval('data.ind'+i+'.stocks')
        var _block = '<div class="stock_rating link">'+
                '<a href="/stocks?industry='+encodeURIComponent(_ind)+'">' + _ind +'</a></div>'+
            '<div>'+
                '<span class="stock_rating ticker head"></span>'+
                '<span class="stock_rating cmp head">CMP</span>'+
                '<span class="stock_rating eps head">EPS</span>'+
                '<span class="stock_rating rs head">RS</span>'+
                '<span class="stock_rating smr head">SMR</span>'+
                '<span class="stock_rating ad head">AD</span>'+
            '</div>' +
            '<div class="industry_stocks">'
        for (let j=0; j<Object.keys(_stock_data).length; j++){
            _block += '<div>'+
                '<span class="stock_rating ticker">'+_stock_data[j].ticker+'</span>'+
                '<span class="stock_rating cmp data">'+_stock_data[j].CMP+'</span>'+
                '<span class="stock_rating eps data">'+_stock_data[j].EPS+'</span>'+
                '<span class="stock_rating rs data">'+_stock_data[j].RS+'</span>'+
                '<span class="stock_rating smr data">'+_stock_data[j].SMR+'</span>'+
                '<span class="stock_rating ad data">'+_stock_data[j].AD+'</span>'+
            '</div>'
        }
        _block += "</div>"
        return _block
    };    
    
}