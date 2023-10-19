function showDevice(installationId) {
    $.ajax({
        url: 'device/' + installationId ,
        type: 'GET',
        success: function (response) {
            console.log("Client show");
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function showList() {
    $.ajax({
        url: 'list',
        type: 'GET',
        success: function (response) {
            console.log("Client show");
        },
        error: function(error) {
            console.log(error);
        }
    });
}
