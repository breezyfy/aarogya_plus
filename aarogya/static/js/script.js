$(document).ready(function() {
    $('#script').DataTable( {
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    } );
} );

function exportPDF() {
    var doc = new jsPDF();
    var specialElementHandlers = {
        '#editor': function (element, renderer) {
            return true;
        }
    };
    doc.fromHTML($('#tableId').get(0), 15, 15, {
        'width': 180,
        'elementHandlers': specialElementHandlers
    });
    doc.save('payments.pdf');
}