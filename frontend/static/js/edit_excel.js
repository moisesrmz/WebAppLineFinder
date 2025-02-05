function cargarHoja() {
    let hoja = document.getElementById("hoja").value;

    fetch("/editor/cargar_hoja", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ hoja: hoja })
    })
    .then(response => response.json())
    .then(data => {
        let table = document.getElementById("excelTable");
        let header = document.getElementById("tableHeader");
        let tbody = table.getElementsByTagName("tbody")[0];

        tbody.innerHTML = "";
        header.innerHTML = "";

        if (data.error) {
            alert(data.error);
            return;
        }

        if (data.length > 0) {
            // 🟢 Agregar columna de numeración
            let thNum = document.createElement("th");
            thNum.innerText = "#";
            header.appendChild(thNum);

            for (let i = 0; i < data[0].length; i++) {
                let th = document.createElement("th");
                th.innerText = `Col ${i + 1}`;
                header.appendChild(th);
            }

            // 🟢 Insertar filas numeradas correctamente
            data.forEach((row, rowIndex) => {
                let newRow = tbody.insertRow();

                // 🟢 Agregar número de fila
                let numCell = newRow.insertCell();
                numCell.innerText = rowIndex + 1;
                numCell.classList.add("text-center", "fw-bold");

                row.forEach(cell => {
                    let newCell = newRow.insertCell();
                    let input = document.createElement("input");
                    input.classList.add("form-control");
                    input.value = cell || "";
                    newCell.appendChild(input);
                });
            });
        }
    })
    .catch(error => {
        console.error("Error al cargar la hoja:", error);
    });
}

// Insertar fila en cualquier posición
function agregarFilaIntermedia() {
    let table = document.getElementById("excelTable").getElementsByTagName("tbody")[0];
    let rowIndex = prompt("¿En qué posición deseas insertar la fila? (1-Número de filas)");

    if (rowIndex && rowIndex > 0 && rowIndex <= table.rows.length) {
        let newRow = table.insertRow(rowIndex - 1);

        // ✅ Agregar celda de numeración (no cuenta como dato real)
        let numCell = newRow.insertCell();
        numCell.innerText = rowIndex;
        numCell.classList.add("text-center", "fw-bold");

        let columns = document.getElementById("tableHeader").getElementsByTagName("th").length - 1;

        for (let i = 0; i < columns; i++) {
            let newCell = newRow.insertCell();
            let input = document.createElement("input");
            input.classList.add("form-control");
            input.value = "";
            newCell.appendChild(input);
        }

        // ✅ Recalcular la numeración de filas
        actualizarNumeracion();
    }
}

// ✅ Recalcular numeración de filas después de insertar/eliminar
function actualizarNumeracion() {
    let table = document.getElementById("excelTable").getElementsByTagName("tbody")[0];

    for (let i = 0; i < table.rows.length; i++) {
        table.rows[i].cells[0].innerText = i + 1;
    }
}

// Insertar columna en cualquier posición
function agregarColumnaIntermedia() {
    let table = document.getElementById("excelTable");
    let header = document.getElementById("tableHeader");
    let tbody = table.getElementsByTagName("tbody")[0];

    let colIndex = prompt("¿En qué posición deseas insertar la columna? (1-Número de columnas)");
    if (colIndex && colIndex > 0 && colIndex <= header.children.length + 1) {
        let th = document.createElement("th");
        let input = document.createElement("input");
        input.classList.add("form-control");
        input.value = `Nueva Col`;
        input.onchange = () => th.innerText = input.value;
        th.appendChild(input);

        header.insertBefore(th, header.children[colIndex - 1]);

        for (let row of tbody.rows) {
            let newCell = row.insertCell(colIndex - 1);
            let input = document.createElement("input");
            input.classList.add("form-control");
            input.value = "";
            newCell.appendChild(input);
        }
    }
}

// Eliminar fila seleccionada
function eliminarFila() {
    let table = document.getElementById("excelTable").getElementsByTagName("tbody")[0];
    let rowIndex = prompt("Ingrese el número de fila a eliminar (1-Número de filas)");
    if (rowIndex && rowIndex > 0 && rowIndex <= table.rows.length) {
        table.deleteRow(rowIndex - 1);
    }
}

// Eliminar columna seleccionada
function eliminarColumna() {
    let table = document.getElementById("excelTable");
    let header = document.getElementById("tableHeader");
    let colIndex = prompt("Ingrese el número de columna a eliminar (1-Número de columnas)");

    if (colIndex && colIndex > 0 && colIndex <= header.children.length) {
        header.removeChild(header.children[colIndex - 1]);
        for (let row of table.getElementsByTagName("tbody")[0].rows) {
            row.deleteCell(colIndex - 1);
        }
    }
}
function guardarCambios() {
    let hoja = document.getElementById("hoja").value;
    let table = document.getElementById("excelTable");
    let tbody = table.getElementsByTagName("tbody")[0];
    let headerRow = document.getElementById("tableHeader").getElementsByTagName("th");
    let datos = [];

    // 🟢 Capturar encabezados
    let encabezados = [];
    for (let i = 1; i < headerRow.length; i++) { // 👈 Saltamos la primera columna de numeración
        encabezados.push(headerRow[i].innerText);
    }
    datos.push(encabezados);  // ✅ Agregamos encabezados como la primera fila de datos

    // 🟢 Capturar los datos de la tabla (sin la columna de numeración)
    for (let row of tbody.rows) {
        let rowData = [];
        for (let i = 1; i < row.cells.length; i++) { // 👈 Saltamos la numeración de filas
            rowData.push(row.cells[i].firstChild.value);
        }
        datos.push(rowData);
    }

    fetch("/editor/guardar_cambios", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ hoja: hoja, datos: datos })
    })
    .then(response => response.json())
    .then(data => alert(data.mensaje));
}
