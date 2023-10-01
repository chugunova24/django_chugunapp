function loadJson(id) {
    return JSON.parse(document.getElementById(id).textContent);
};

function loadCsv(id) {
    return document.getElementById(id).textContent;
};







function filterSelectFile(jsonData) {
    idSelectColumnsOfFile.innerHTML = "<option value='0' disabled>Select column list</option>";
        mychange = idSelectFile.value;

        if (idSelectColumnsOfFile.length != 0) {
            for (var i = 0; i < jsonData.length; i++) {
                if (jsonData[i].file_id == mychange) {

                    idSelectColumnsOfFile.innerHTML += `<option value="${jsonData[i].id}">${jsonData[i].name}</option>`;

                }
            }

        } else {
            idSelectColumnsOfFile.disabled = true;
        }
}


function filterColumnsFile() {
    let selectedOptions = idSelectColumnsOfFile.selectedOptions;
    idSelectSortBy.innerHTML = "<option value='0' disabled>Select column</option>";

    for (var i = 0; i < selectedOptions.length; i++) {
        idSelectSortBy.innerHTML += `<option value="${selectedOptions[i].value}">${selectedOptions[i].text}</option>`;
    }

}


function filterSelectedItems(jsonData) {
    // let jsonData = loadJson('jsonFilesData');
    // let jsonData = jsonData;

    idSelectFile.onchange = function () {
        idSelectColumnsOfFile.innerHTML = "<option value='0' disabled>Select column list</option>";
        idSelectSortBy.innerHTML = "<option value='0' disabled></option>";
        mychange = idSelectFile.value;

        if (idSelectColumnsOfFile.length != 0) {
            for (var i = 0; i < jsonData.length; i++) {
                if (jsonData[i].file_id == mychange) {
                    idSelectColumnsOfFile.innerHTML += `<option value="${jsonData[i].id}">${jsonData[i].name}</option>`;
                }
            }

        } else {
            idSelectColumnsOfFile.disabled = true;
            idSelectSortBy.disabled = true;
        }
    };

    idSelectColumnsOfFile.onchange = function () {
        let selectedOptions = idSelectColumnsOfFile.selectedOptions;
        idSelectSortBy.innerHTML = "<option value='0' disabled>Select column</option>";

        for (var i = 0; i < selectedOptions.length; i++) {
            idSelectSortBy.innerHTML += `<option value="${selectedOptions[i].value}">${selectedOptions[i].text}</option>`;
        }
        idSelectSortBy.disabled = false;

    };
}



function generateFile() {

    idBtnGenerateFile.addEventListener("click", (event) => {
        let arr = [idSelectFile, idSelectColumnsOfFile, idSelectSortBy];

        let data = "";
        let haveEmptyField = false;

        for (var i=0; i < arr.length; i++) {
            piece = `&${$(arr[i]).serialize()}`;

            if (piece.length === 1 || piece.length === 0) {
                haveEmptyField = true;
                break;
            };

            data += piece;

        };

        data += `&${idBtnGenerateFile.name}`;


        if (!haveEmptyField) {

            idDivError.innerHTML = "";

            $.ajax({
                method: 'get',
                data: data,
                async: true,
                timeout: 10000, // 20 sec
                success: function (result) {
                    if (idBtnDownload.style.display == "none") idBtnDownload.style.display = "";
                    $('#divRenderTable').html($(result).find('#divRenderTable').html());
                    $('#idTableCsv').html($(result).find('#idTableCsv').html());
                    $('#idDivError').html($(result).find('#idDivError').html());

                    let count = $('th[colspan="3"]').length;

                    for (let j = 0; j < count; j++) {
                        let pattern = "#idError" + j;
                        $(pattern).html($(result).find(pattern).html());
                    }
                }
            });

        } else {

            idDivError.innerHTML = '<p class="text-danger"><strong>Options is empty</strong></p>';

        }


    });
}






function unescapeHtml(safe) {
    return safe
        .replaceAll("&amp;", "&")
        .replaceAll("&lt;", "<")
        .replaceAll("&gt;", ">")
        .replaceAll("&quot;", '"')
        //         .replaceAll("&#039;", "'");
        .replaceAll("&#x27", "'");
}


function downloadFile(data, name = "filtered_table.csv") {


    data = unescapeHtml(data);
    const BOM = new Uint8Array([0xEF, 0xBB, 0xBF]);
    const blob = new Blob([BOM, data], {type: "text/csv;charset=utf-8"});


    const href = URL.createObjectURL(blob);

    const a = Object.assign(document.createElement("a"), {
        href,
        style: "display:none",
        download: name,
    });

    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(href);
    a.remove();

}



window.onload = function () {
    let jsonData = loadJson('jsonFilesData');

    idSelectColumnsOfFile.innerHTML = "<option value='0' disabled>Select column list</option>";
    selectValue = idSelectFile.value;
    idSelectSortBy.innerHTML = "<option value='0' disabled></option>";
    idSelectSortBy.disabled = true;
    console.log(`idSelectSortBy.disabled: ${idSelectSortBy.disabled}`)

    if (idSelectColumnsOfFile.length != 0) {
        for (var i = 0; i < jsonData.length; i++) {
            if (jsonData[i].file_id == selectValue) {

                idSelectColumnsOfFile.innerHTML += `<option value="${jsonData[i].id}">${jsonData[i].name}</option>`;
            }
        }
    } else {
        idSelectColumnsOfFile.disabled = true;
    };


    filterSelectedItems(jsonData);
    generateFile();

    idBtnDownload.addEventListener("click", (event) => {
        let csvText = loadCsv('idTableCsv');
        downloadFile(data = csvText, name = "filtered_table.csv");
    });



}


// window.onload = function () {
//     let jsonData = loadJson('jsonFilesData');
//
//     function filterItemsInit() {
//         filterSelectFile(jsonData);
//         filterColumnsFile();
//
//
//     }
//
//     filterSelectedItems();
//     generateFile();
//
//     idBtnDownload.addEventListener("click", (event) => {
//         let csvText = loadCsv('idTableCsv');
//
// //        if () ПРОВЕРКА НА ПУСТОТУ И NONE
//
//         downloadFile(data = csvText, name = "filtered_table.csv");
//     });
//
// }
