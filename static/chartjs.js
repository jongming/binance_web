class RSChartjs{
    constructor(data_array){
        this.data_array = data_array;
    }

    build_chart(){
        if (this.data_array != null){
            new Chart(document.getElementById(this.data_array[0]), {
                type: "line",
                data: {
                    labels: this.data_array[1], //date
                    datasets:[{
                        label: "CMP",
                        data: this.data_array[3],
                        fill: false,
                        borderColor: "rgb(255, 0, 0)",
                        tension: 0.1,
                        showLine: true
                    },
                    {
                        label: "EPS", //EPS
                        data: this.data_array[5],
                        fill: false,
                        borderColor: "rgb(0, 145, 0)",
                        tension: 0.1,
                        showLine: true
                    },
                    {
                        label: "RS", //RS
                        data: this.data_array[7],
                        fill: false,
                        borderColor: "rgb(0, 0, 255)",
                        tension: 0.1,
                        showLine: true
                    },
                    {
                        label: "SMR", //SMR
                        data: this.data_array[9],
                        fill: false,
                        borderColor: "rgb(255, 153, 51)",
                        borderDash: [5, 5],
                        tension: 0.1,
                        showLine: true
                    },
                    {
                        label: "A/D", //AD
                        data: this.data_array[11],
                        fill: false,
                        borderColor: "rgb(200, 0, 200)",
                        borderDash: [5, 5],
                        tension: 0.1,
                        showLine: true
                    },
                ]
                    
                },
                options:{
                    responsive: true,
                    maintainAspectRatio: false
                }
        });
        }
    }
}

class RSChartjs_creator{
    constructor(rs_data){
        this.rs_data = rs_data;
        this.data_array = []
    }

    process_data(){
        const _data_array = []
        //build array for chartjs    
        for (let i=0; i<Object.keys(this.rs_data).length; i++){
            var _array = eval('["chjs_chart'+i+'", rs_data.stock'+i+'.date, "CMP", rs_data.stock'+i+'.cmp, "EPS", rs_data.stock'+i+'.eps, "RS", rs_data.stock'+i+'.rs, "SMR", rs_data.stock'+i+'.smr_value, "AD", rs_data.stock'+i+'.ad_value]')
            _data_array.push(_array)
        }
        this.data_array = _data_array
    }

    //create chartjs object based on the number of tickers
    apply_chart(){
        for (var i=0; i< this.data_array.length; i++){
            var new_chart = document.createElement('chart');
            new_chart = new RSChartjs(this.data_array[i]);
            new_chart.id = "chjs_chart"+ i;
            new_chart.build_chart();
        }
    }

}

class IndustryChartjs{
    constructor(data_array){
        this.data_array = data_array
    }

    build_chart(){
        if (this.data_array != null){
            new Chart(document.getElementById(this.data_array[0]), { //match div id
                type: "line",
                data: {
                    labels: this.data_array[2], //industry
                    datasets:[{
                        label: this.data_array[1],
                        data: this.data_array[3],
                        fill: false,
                        borderColor: "rgb(255, 0, 0)",
                        tension: 0.1,
                        showLine: true
                    },
                ]
                    
                },
                options:{
                    responsive: true,
                    maintainAspectRatio: false
                }
        });
        }
    }
}

class IndustryChartjs_creator{
    constructor(jindustry_data){
        this.jindustry_data = jindustry_data;
        this.data_array = []
    }

    process_data(){
        const charts_structure = []
        for (let i=0; i<Object.keys(this.jindustry_data).length; i++){
            var _ind = eval('jindustry_data.ind'+i+'.industry')
            var _on_date = eval('jindustry_data.ind'+i+'.on_date')
            // var _perfT = eval('jindustry_data.ind'+i+'.perfT')
            var _perfT = eval('jindustry_data.ind'+i+'.close')
            var _array = eval('["chjs_chart'+i+'", _ind, _on_date, _perfT]')
            // var _array = eval('["chjs_chart'+i+'", _ind, _on_date, _close]')
            charts_structure.push(_array)
        }
        this.data_array = charts_structure
        console.log(this.data_array)
    }

    apply_chart(){
        for (let i=0; i< this.data_array.length; i++){
            var new_chart = document.createElement('chart');
            new_chart = new IndustryChartjs(this.data_array[i]);
            new_chart.id = "chjs_chart"+ i;
            new_chart.build_chart();
        }
    }
}