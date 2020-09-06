var initOutagesTable = function(outageInfoRows) {
    var tableCols = []
    $.each(outageInfoRows[0], function(key, value) {
        var colMeta = {};
        colMeta.data = key;
        colMeta.title = key;
        tableCols.push(colMeta);
    });

    $('#outagesTable').DataTable({
        data: outageInfoRows,
        columns: tableCols,
        pageLength: 100,
        dom: 'Bfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pageLength'
        ]
    });
};