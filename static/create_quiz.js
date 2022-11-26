// create_quiz.js
// Created by Dan Glendon, October 17th 2022
// This loads along with create_quiz.html and allows a user (employer) to create a quiz to be sent to potential candidates.
// It is flexible, as it doesn't suggest questions and just allows input.
// Please note, the style as of right now is temporary. It will be changed in the future.

// Websites used for solutions and inspiration in this file:
// https://codepen.io/Kanecodes/pen/EeejJv
// https://stackoverflow.com/questions/16715075/preventing-multiple-clicks-on-button

// Once the window is loaded run the beginning code.
// Note that without this, the script runs before the DOM loads
// and it can't find the buttons to add click events to.
window.onload=function(){

// Screen 1, where you click "Create Question" or submit the finished quiz
var configContainer = document.getElementById('configContainer');
var createButton = document.getElementById('createButton');
var nextButton = document.getElementById('nextButton');
var numberOfQuestions = document.getElementById('numberOfQuestions');
var questions = [["0", "0", "0", "0", "0"] * 100];
var position = 0;
var successText = document.getElementById('successText');

// Screen 2, where you pick what type of question you want to make
var chooseContainer = document.getElementById('chooseContainer');
var multipleChoice = document.getElementById('multipleChoice');
var shortAnswer = document.getElementById('shortAnswer');
var checkAll = document.getElementById('checkAll');
var trueOrFalse = document.getElementById('trueOrFalse');
var type = ""

// Screen 3, where you type in the questions and answers you want
var inputQuestion = document.getElementById('inputQuestion');
var answerOne = document.getElementById('inputOne');
var answerTwo = document.getElementById('inputTwo');
var answerThree = document.getElementById('inputThree');
var answerFour = document.getElementById('inputFour');
var inputAnswer = document.getElementById('inputAnswer');
var questionText = document.getElementById('questionText');
var answerOneText = document.getElementById('answerOneText');
var answerTwoText = document.getElementById('answerTwoText');
var answerThreeText = document.getElementById('answerThreeText');
var answerFourText = document.getElementById('answerFourText');
var inputAnswerText = document.getElementById('correctAnswerText');
var inputAnswerTextTF = document.getElementById('correctAnswerTrueFalse');
var inputAnswerTF = document.getElementById('inputAnswerTrueFalse');
var inputAnswerTextTF = document.getElementById('correctAnswerTrueFalse');
var inputAnswerTF = document.getElementById('inputAnswerTrueFalse');
var addButton = document.getElementById('addButton');

// Screen 4, where you put in the name of the test and employer
var inputTestName = document.getElementById('inputTestName')
var inputEmployer = document.getElementById('inputEmployer')
var inputEmail = document.getElementById('inputEmail')
var submitButton = document.getElementById('submitButton')
var nameEmployerContainer = document.getElementById('nameEmployerContainer')
var testName = ""
var employer = ""
var email = ""

// Screen 1 Buttons
if (createButton) {
createButton.addEventListener('click', () => {
    if (position <= 100) {
        hideConfiguration();
        unhideChoose();
    } else {
        alert('Too many questions');
    }
})}

if (nextButton) {
    nextButton.addEventListener('click', () => {
        if (position == 0) {
            alert('Your quiz has zero questions. Please add some.');
        } else {
            hideConfiguration();
            unhideInputNames();
        }
})}

if (submitButton) {
    submitButton.addEventListener('click', () => {
        if (inputTestName.value == "") {
            alert('Please enter a test name.');
        } else if (inputTestName.value == "") {
            alert('Please enter an employer name.');
        } else if (inputEmail.value == "") {
            alert('Please enter a valid email address.');
        } else {
            testName = inputTestName.value
            employer = inputEmployer.value
            email = inputEmail.value
            hideInputNames();
            showSuccess();
            submitQuiz();
        }
    })}


// Screen 2 Type Buttons
multipleChoice.addEventListener('click', () => {
    hideChoose();
    unhideMultipleChoiceOrCheckAll();
    switchToScreen();
    type = "multipleChoice"
})

shortAnswer.addEventListener('click', () => {
    hideChoose();
    unhideShortAnswer();
    unhideShortAnswer();
    switchToScreen();
    type = "shortAnswer"
})

checkAll.addEventListener('click', () => {
    hideChoose();
    unhideMultipleChoiceOrCheckAll();
    switchToScreen();
    type = "checkAll"
})

trueOrFalse.addEventListener('click', () => {
    hideChoose();
    unhideTrueFalse();
    unhideTrueFalse();
    switchToScreen();
    type = "trueOrFalse"
})

backButton.addEventListener('click', () => {
    hideChoose();
    unhideConfiguration();
})

// Screen 3 Add Button
if (addButton) {
    addButton.addEventListener('click', () => {
        //TODO: If any fields are empty, don't continue
        if (1 == 2) {
            alert('Fields need to be filled before submission.');
            return
        }
        else if (type == "multipleChoice" && inputAnswer.value != "A" && inputAnswer.value != "B" && inputAnswer.value != "C" && inputAnswer.value != "D") {
            alert('Please fill in an answer A, B, C, or D for correct answer.')
        } else if (type == "trueOrFalse" && inputAnswerTF.value != "T" && inputAnswerTF.value != "F" && inputAnswerTF.value != "True" && inputAnswerTF.value != "False") {
            alert('Please fill in either "True" (T) or "False" (F) for correct answer.')
            return
        }
        else if (type == "multipleChoice" && inputAnswer.value != "A" && inputAnswer.value != "B" && inputAnswer.value != "C" && inputAnswer.value != "D" && inputAnswer.value != "") {
            alert('Please fill in an answer A, B, C, or D for correct answer.')
        } else if (type == "trueOrFalse" && inputAnswerTF.value != "T" && inputAnswerTF.value != "F" && inputAnswerTF.value != "True" && inputAnswerTF.value != "False" && inputAnswerTF.value != "") {
            alert('Please fill in either "True" (T) or "False" (F) for correct answer.')
        } else {
        addButton.disabled = true;
        addButton.disabled = true;
            switch (type) {
            case 'checkAll':
                createMultipleChoiceOrCheckAll();
                break;
            case 'shortAnswer':
                createShortAnswer();
                createShortAnswer();
                break;
            case 'multipleChoice':
                createMultipleChoiceOrCheckAll();
                break;
            case 'trueOrFalse':
                createTrueFalse();
                createTrueFalse();
                break;
            }
            addQuestion();
            hideQuestionFill();
            unhideConfiguration();
            clearQuiz();
            type = ""
        }
    })}

// Third screens where you fill in the question and answers

function switchToScreen() {
    addButton.disabled = false;
}

function createMultipleChoiceOrCheckAll() {
    questions[position] = []
    questions[position][0] = type
    questions[position][1] = inputQuestion.value
    questions[position][2] = inputOne.value
    questions[position][3] = inputTwo.value
    questions[position][4] = inputThree.value
    questions[position][5] = inputFour.value
    questions[position][6] = inputAnswer.value
}

function createTrueFalse() {
    questions[position] = []
    questions[position][0] = type
    questions[position][1] = inputQuestion.value;
    questions[position][6] = inputAnswerTF.value;
}

function createShortAnswer() {
    questions[position] = []
    questions[position][0] = type
    questions[position][1] = inputQuestion.value;
}

function addQuestion() {
    position += 1;
    last_type = questions[position-1][0]
    if (last_type == "multipleChoice") {
        add = "Multiple Choice"
    } else if (last_type == "shortAnswer") {
        add = "Short Answer"
    } else if (last_type == "checkAll") {
        add = "Check All That Apply"
    } else if (last_type == "trueOrFalse") {
        add = "True or False"
    }
    lastQuestion.innerHTML = 'Your last submitted question was: ' + add
    if (position == 1) {
        numberOfQuestions.innerHTML = 'Your quiz currently has 1 question.' 
    } else {
        numberOfQuestions.innerHTML = 'Your quiz currently has ' + position + ' questions.'
    }
    
}

function submitQuiz() {
    fetch("/submit_quiz", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify([questions, employer, testName, email])
    }).then(res => {
        console.log("Quiz Submitted! Response:", res);
    });
}

var clearForm = () => { form.classList.add('hide'); }
var clearQuiz = () => { 
    answerOne.innerHTML = '', 
    answerTwo.innerHTML = '', 
    answerThree.innerHTML = '', 
    answerFour.innerHTML = ''

    var elements = document.getElementsByTagName("input");

    for (var i = 0; i < elements.length; i++) {
            elements[i].value = ''
    }
}

var hideConfiguration = () => {
    configContainer.classList.add('hide')
}

var hideChoose = () => {
    chooseContainer.classList.add('hide')
}

var hideQuestionFill = () => { 
    inputQuestion.classList.add('hide');
    answerOne.classList.add('hide');
    answerTwo.classList.add('hide');
    answerThree.classList.add('hide');
    answerFour.classList.add('hide');
    questionText.classList.add('hide');
    answerOneText.classList.add('hide');
    answerTwoText.classList.add('hide');
    answerThreeText.classList.add('hide');
    answerFourText.classList.add('hide');
    inputAnswerText.classList.add('hide');
    inputAnswer.classList.add('hide');
    addButton.classList.add('hide');
    inputAnswerTextTF.classList.add('hide');
    inputAnswerTF.classList.add('hide');
    inputAnswerTextTF.classList.add('hide');
    inputAnswerTF.classList.add('hide');
}

var unhideInputNames = () => {
    nameEmployerContainer.classList.remove('hide')
}

var hideInputNames = () => {
    nameEmployerContainer.classList.add('hide')
}

var unhideConfiguration = () => { 
    configContainer.classList.remove('hide');
}

var unhideChoose = () => { 
    chooseContainer.classList.remove('hide');
}

var unhideMultipleChoiceOrCheckAll = () => { 
    inputQuestion.classList.remove('hide');
    answerOne.classList.remove('hide');
    answerTwo.classList.remove('hide');
    answerThree.classList.remove('hide');
    answerFour.classList.remove('hide');
    questionText.classList.remove('hide');
    answerOneText.classList.remove('hide');
    answerTwoText.classList.remove('hide');
    answerThreeText.classList.remove('hide');
    answerFourText.classList.remove('hide');
    inputAnswerText.classList.remove('hide');
    inputAnswer.classList.remove('hide');
    addButton.classList.remove('hide');
}

var unhideTrueFalse = () => { 
    questionText.classList.remove('hide');
    inputQuestion.classList.remove('hide');
    inputAnswerTextTF.classList.remove('hide');
    inputAnswerTF.classList.remove('hide');
    addButton.classList.remove('hide');
}

var unhideTrueFalse = () => { 
    questionText.classList.remove('hide');
    inputQuestion.classList.remove('hide');
    inputAnswerTextTF.classList.remove('hide');
    inputAnswerTF.classList.remove('hide');
    addButton.classList.remove('hide');
}

var unhideShortAnswer = () => { 
    questionText.classList.remove('hide');
    inputQuestion.classList.remove('hide');
    addButton.classList.remove('hide');
}

var showSuccess = () => {
    successText.classList.remove('hide');
}
}
