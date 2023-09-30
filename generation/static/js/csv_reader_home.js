
//$(document).ready(function() {
//   let btnInfo = $('#id-btn-info');
//
//
//   btnInfo.click(function(e) {
//       let btnInfoName = "_info";
//       let data = $(form).serialize() + `&${btnInfoName}`; // Данные формы
//
//       $.ajax({
//           method: 'get',
//           data: data,
//           async: true,
//           timeout: 10000, // 10 sec
//           success: function(result){
//                $(divInfo).html($(result).find(divInfo).html());
//           }
//        });
//
//    });
//});



$(document).ready(function() {
   let form = $('#formSelectFiles');
   let btnInfo = $('#id-btn-info');
   let btnFilter = $('#id-btn-filter');
   let divInfo = '#ModalInfoTable';

   btnInfo.click(function(e) {
       let btnInfoName = "_info";
       let data = $(form).serialize() + `&${btnInfoName}`; // Данные формы

       $.ajax({
           method: 'get',
           data: data,
           async: true,
           timeout: 10000, // 10 sec
           success: function(result){
                $(divInfo).html($(result).find(divInfo).html());
           }
        });

       var ModalInfoTable = new bootstrap.Modal(document.getElementById('ModalInfoTable'), {
         keyboard: true,
         backdrop: true,
         focus: true,

       });

       ModalInfoTable.show();
    });



   btnFilter.click(function(e) {
       let idSelectFiles = $('#id_select_file');
       let url = "/file-reader/csv-reader-filter";
       let data = `?${idSelectFiles.serialize()}`;

       window.location.href = `${url}${data}`;
    });





});


// $(document).ready(function() {
//    let form = $('#formSelectFiles');
//    let btnFilter = $('#id-btn-filter');
//
//    btnFilter.click(function(e) {
//        let btnFilter = "_filter";
//        let data = $(form).serialize() + `&${btnFilter}`; // Данные формы
//
//        $.ajax({
//            method: 'get',
//            data: data,
//            async: true,
//            timeout: 10000, // 10 sec
//            // success: function(result){
//            //
//            // }
//         });
//
//
//     });
// });





