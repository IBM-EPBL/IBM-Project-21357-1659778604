let x = 0;

const editCv = () => {
  document.getElementById("editor").style =
    "background-color: #f5f5f5; color: #000;border: 1px solid #000;border-radius: 5px;transition: 0.5s;";
  x = 1;
  // loop res_details
  let res_details = document.getElementsByClassName("res_details");
  for (let i = 0; i < res_details.length; i++) {
    res_details[i].contentEditable = "true";
  }

  var id = document.getElementById("img_clk");
  id.onclick = function () {
    let imgData = prompt("Enter image URL");
    checkIfImageExists(imgData, (exists) => {
      if (exists) {
        id.src = imgData;
      } else {
        alert("Image does not exists.");
      }
    });
  };
};
function changeBarWidth(id) {
  if (x == 1) {
    a = prompt("Enter in %");
    document.getElementById(id).style.width = a;
  }
}

function printPageArea(areaID) {
  var printContent = document.getElementById(areaID);
  var WinPrint = window.open("", "", "width=900,height=650");

  WinPrint.document.write(
    '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Resume</title><script src="https://kit.fontawesome.com/1625eab60d.js" crossorigin="anonymous"></script><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet"integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous" ><link rel="stylesheet" href="style.css"></head>'
  );
  WinPrint.document.write(
    '<link rel="stylesheet" href="style.css" type="text/css"/>'
  );
  WinPrint.document.write(printContent.innerHTML);
  WinPrint.document.close();
  WinPrint.focus();
  WinPrint.print();
  WinPrint.close();
}

// CHECK IF IMAGE EXISTS
function checkIfImageExists(url, callback) {
  const img = new Image();
  img.src = url;

  if (img.complete) {
    callback(true);
  } else {
    img.onload = () => {
      callback(true);
    };

    img.onerror = () => {
      callback(false);
    };
  }
}