
function pictuerHedler(picture) {
    picture.multiple = "true";
}
function kwHedler(kw) {
    kw.required = "true";
    var eleTitle = document.createElement('span');
    eleTitle.style.color = "red";
    eleTitle.style.fontSize = "1-5px";
    eleTitle.innerHTML = '*';
    kw.before(eleTitle);
}

function inputSetting() {
    var content = document.getElementsByTagName("textarea")[0];
    var inputList = document.getElementsByTagName("input");
    for (var i = 0; i < inputList.length; i++) {
        if(inputList[i].name=="email" || inputList[i].name=="title"){
            var kw = inputList[i];
            kwHedler(kw);
        }
        else if (inputList[i].name=="picture"){
            var picture = inputList[i];
            pictuerHedler(picture);
        }
        else{}
    }
    kwHedler(content)
}
inputSetting();

