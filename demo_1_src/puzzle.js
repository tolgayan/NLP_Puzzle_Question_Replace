var txt = '';
var txtList;
var xmlhtpp = new XMLHttpRequest();
xmlhtpp.onreadystatechange = function(){
    txt = xmlhtpp.responseText;
    txtList = txt.split("\n");
    console.log(txtList);
    var i;
    for(i = 0; i < 37; i++) {
        if( i < 25){
            if(txtList[i].trim() == "-1".trim()){
                var j = i + 1;
                document.getElementById("p" + j).innerHTML = "";
                document.getElementById("cell" + j).style.background = "#000";
            } else {
                if(txtList[i].length < 4){
                    var j = i + 1;
                    document.getElementById("p" + j).innerHTML = txtList[i];
                } else {
                    var j = i + 1;
                    document.getElementById("n" + j).innerHTML = txtList[i].charAt(0);
                    document.getElementById("p" + j).innerHTML = txtList[i].charAt(2);
                }
            }
        } else if ( i > 25 && i < 31 ) {
            var j = i - 25
            document.getElementById("a" + j).innerHTML = txtList[i];
        } else if (i > 31 && i < 37 ) {
            var j = i - 31
            document.getElementById("d" + j).innerHTML = txtList[i];
        }
    }


};
document.getElementById("date").innerHTML = Date().substring(0,25);
xmlhtpp.open("GET","PuzzleInfo.txt", true);
xmlhtpp.send();



