function get_metadata(value) {
    $.ajax({
        url: '/metadata/' + value,
        success: function (response) {
            console.log(response);
            document.getElementById('age').innerText = response.AGE;
            document.getElementById('bbtype').innerText = response.BBTYPE;

            document.getElementById('gender').innerText = response.GENDER;
            document.getElementById('location').innerText = response.LOCATION;
            document.getElementById('sample').innerText = response.SAMPLEID;
        },
        error: function (error) {
            console.log(error);
        }
    });

}
$(function () {
    $.ajax({
        url: '/names',
        success: function (response) {
            var select = document.getElementById("selDataset");
            for (var i = 0; i < response.length; i++) {
                var option = document.createElement("option");
                option.text = response[i];
                select.add(option);
            }

        },
        error: function (error) {
            console.log(error);
        }
    });

});

function optionChanged(value) {
    get_metadata(value);
    $.ajax({
        url: '/samples/' + value,
        success: function (response) {
            var datas = [{
                values: response.sample_values,
                labels: response.otu_ids,
                type: 'pie'
            }];

            var layout = {
                height: 700,
            };
            TESTER = document.getElementById('pai');
            Plotly.newPlot(TESTER, datas, layout);


            var trace1 = {
                x: response.otu_ids,
                y: response.sample_values,
                mode: 'markers',
                marker: {
                    color: response.otu_ids,

                    size: response.sample_values
                }
            };

            var data1 = [trace1];

            var layout1 = {
                title: 'Marker Size and Color',
                showlegend: false,
            };

            Plotly.newPlot('bubble', data1, layout1);


        },
        error: function (error) {
            console.log(error);
        }
    });

}


