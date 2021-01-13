var sideMenuOpen = false;

function openSideMenu(){
    document.getElementById("sideNav").style.width = "80%";
    sideMenuOpen = true;
}

function closeSideMenu(){
    if(sideMenuOpen){
        document.getElementById("sideNav").style.width = "0%";
        sideMenuOpen = false;
    }
    
}



//CREATEWORKOUTPLAN/ADDEXERCISES

var numOfExercises = 1;

function addExerciseToForm(){
    //get hold of the container
    numOfExercises++;
    var container = document.getElementById("exerciseInputs");
    var className = "exercise" + numOfExercises;
    var input = createExerciseForm(className);
    container.appendChild(input);
    var footer = document.getElementById("pageFooter");
    footer.style.display = "none";
}

function createExerciseForm(name){
    var div = document.createElement('div');
    div.className = name;
    div.id = name;
    num = numOfExercises;
    div.innerHTML = `<label for="picOfExercise${num}">Picture or Video of Exercise For User Clarity: </label>
    <input type="file" id="picOfExercise${num}" name="picOfExercise${num}" accept="image/*, video/*">
    <br>
    <br>
    <label for="exerciseName${num}">Exercise Name: </label>
    <input type="text" id="exerciseName${num}" name="exerciseName${num}">
    <br>
    <br>
    <label for="sets${num}">Sets</label>
    <select name="sets${num}" id="sets${num}">
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
        <option value="6">6</option>
        <option value="7">7</option>
        <option value="8">8</option>
        <option value="9">9</option>
        <option value="10">10</option>
    </select>
    <br>
    <br>
    <label for="sameRepsPerSet${num}">Same Number of Reps For Every Set? </label>
    <input type="checkbox" id="sameRepsPerSet${num}" name="sameRepsPerSet${num}" onclick="loadNumberOfSets" checked>
    <br>
    <br>
    <div id="repsPerSet${num}">
        <label for="repsPerSet${num}">Reps Per Set</label>
        <input type="number" id="reps${num}" name="reps${num}">
    </div> 
    <br>
    <label for="notesOnExercise${num}">Notes On Exercise</label>
    <textarea id="notesOnExercise${num}" name="notesOnExercise${num}" placeholder="Input guidance on the exercise, what you want the user to focus on during the exercise, or anything that you believe would be beneficial for the user to know before beginning the exercise" rows="4" cols="100"></textarea>
    <br>
    <hr/>
    <br>`
    return div;
}

function removeExerciseFromForm(){
    var container = document.getElementById("exerciseInputs");
    container.removeChild(container.lastChild);
    numOfExercises--;
}

function scrollToBottom(){
    console.log(`exercise${numOfExercises}`);
    document.getElementById(`exercise${numOfExercises}`).scrollIntoView();
}