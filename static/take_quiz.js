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

    var questions = [];

    function loadQuestions() {
        questions_json = document.getElementById('questionsImport').innerHTML;
        for (var i in questions_json) {
            questions.push([i]);
        }
    }

    function dummy_loadQuestions() {
        questions = [["multipleChoice", "What is the question?", "Hello?", "Yes?", "What?", "The question!", "A"], 
        ["shortAnswer", "Please type something."],
        ["checkAll", "How many numbers are one digit?", "12", "6", "3", "43"],
        ["trueOrFalse", "Is this a quiz?"]]
    }

    dummy_loadQuestions();

    // Screen 3, where you type in the questions and answers you want
    var welcomeText = document.getElementById('welcomeText');
    var takeButton = document.getElementById('takeButton');
    var inputQuestion = document.getElementById('inputQuestion');
    var inputOneText = document.getElementById('inputOneLabel');
    var inputOne = document.getElementById('inputOne')
    var inputTwoText = document.getElementById('inputTwoLabel');
    var inputTwo = document.getElementById('inputTwo')
    var inputThreeText = document.getElementById('inputThreeLabel');
    var inputThree = document.getElementById('inputThree')
    var inputFourText = document.getElementById('inputFourLabel');
    var inputFour = document.getElementById('inputFour')
    var inputOneCA = document.getElementById('inputOneCALabel');
    var inputTwoCA = document.getElementById('inputTwoCALabel');
    var inputThreeCA = document.getElementById('inputThreeCALabel');
    var inputFourCA = document.getElementById('inputFourCALabel');
    var inputFourCA = document.getElementById('inputFourCALabel');
    var addButton = document.getElementById('addButton');
    var questionContainer = document.getElementById('questionContainer');
    var multipleChoiceContainer = document.getElementById('MultipleChoiceContainer');
    var trueFalseContainer = document.getElementById('TrueFalseContainer');
    var checkAllContainer = document.getElementById('CheckAllContainer');
    var inputShort = document.getElementById('inputShort');
    var scoreText = document.getElementById('scoreText');
    var disclaimer = document.getElementById('disclaimer');
    
    var type = "welcome";
    var position = 0;
    var score = 0;
    var totalMC = 0



    function nextQuestion() {
        if (type == "checkAll") {
            hideCheckAll()
        } else if (type == "multipleChoice") {
            hideMultipleChoice()
        } else if (type == "shortAnswer") {
            hideShortAnswer()
        } else if (type == "trueOrFalse") {
            hideTrueOrFalse()
        } else if (type == "welcome") {
            hideWelcome()
            unhideQuestion()
        }
        uncheck();

        if (position > questions.length-1) {
            hideQuestion()
            showSuccess()
        }
        else if (questions[position][0] == "checkAll") {
            inputQuestion.innerHTML = questions[position][1];
            inputOneCA.innerHTML = questions[position][2];
            inputTwoCA.innerHTML = questions[position][3];
            inputThreeCA.innerHTML = questions[position][4];
            inputFourCA.innerHTML = questions[position][5];
            unhideCheckAll();
            type = "checkAll"
        }
        else if (questions[position][0] == "multipleChoice") {
            inputQuestion.innerHTML = questions[position][1];
            inputOneText.innerHTML = questions[position][2];
            inputTwoText.innerHTML = questions[position][3];
            inputThreeText.innerHTML = questions[position][4];
            inputFourText.innerHTML = questions[position][5];
            unhideMultipleChoice();
            type = "multipleChoice"
        }
        else if (questions[position][0] == "trueOrFalse") {
            inputQuestion.innerHTML = questions[position][1];
            unhideTrueOrFalse();
            type = "trueOrFalse"
        }
        else if (questions[position][0] == "shortAnswer") {
            inputQuestion.innerHTML = questions[position][1];
            unhideShortAnswer();
            type = "shortAnswer"
        }
    }

    function uncheck() {
        var elements = document.getElementsByTagName("input");

        for (var i = 0; i < elements.length; i++) {
                if (elements[i].type == "radio") {
                    elements[i].checked = false;
                }
                if (elements[i].type == "checkbox") {
                    elements[i].checked = false;
                }
        }
        inputShort.innerHTML = ''
    }

    // Submit Question Button
    if (addButton) {
        addButton.addEventListener('click', () => {
            //TODO: If any fields are empty, don't continue
            if (1 == 2) {
                alert('Please submit an answer to the question.');
            } else {
                // TODO: Add "check all" status into the form somewhere
                checkCorrectness();
                addButton.disabled = true;
                position += 1;
                nextQuestion();
                switchToScreen();
            }
        })}

    function checkCorrectness() {
        // Only works for multiple choice
        if (type == "multipleChoice") {
            correctAns = questions[position][6]
            if (inputOne.checked == true) {
                theirAns = "A"
            } else if (inputTwo.checked == true) {
                theirAns = "B"
            } else if (inputThree.checked == true) {
                theirAns = "C"
            } else if (inputFour.checked == true) {
                theirAns = "D"
            }
            if (theirAns == correctAns) {
                score += 1
            }
            totalMC += 1
        }
    }

    // Initiation Button
    if (takeButton) {
        takeButton.addEventListener('click', () => {
            //TODO: If any fields are empty, don't continue
            if (1 == 2) {
                alert('Please submit an answer to the question.');
            } else {
                // TODO: Add "check all" status into the form somewhere
                takeButton.disabled = true;
                nextQuestion();
                switchToScreen();
            }
        })}

    function switchToScreen() {
        addButton.disabled = false;
    }
    
    function submitQuiz() {
        fetch("/submit_quiz_answers", {
            method: "POST",
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify(score)
        }).then(res => {
            console.log("Quiz Submitted! Response:", res);
        });
        window.location.href = "/"
    }
    
    var clearForm = () => { form.classList.add('hide'); }
    var clearQuiz = () => { 
        inputShort.innerHTML = ''
    }
    
    var hideWelcome = () => { 
        welcomeText.classList.add('hide');
        takeButton.classList.add('hide');
    }   
    
    var hideCheckAll = () => { 
        inputOneCA.classList.add('hide');
        inputTwoCA.classList.add('hide');
        inputThreeCA.classList.add('hide');
        inputFourCA.classList.add('hide');
        checkAllContainer.classList.add('hide');
        addButton.classList.add('hide');
    }
    
    var unhideCheckAll = () => { 
        inputOneCA.classList.remove('hide');
        inputTwoCA.classList.remove('hide');
        inputThreeCA.classList.remove('hide');
        inputFourCA.classList.remove('hide');
        checkAllContainer.classList.remove('hide');
        addButton.classList.remove('hide');
    }
    
    var hideMultipleChoice = () => { 
        addButton.classList.add('hide');
        multipleChoiceContainer.classList.add('hide')
    }
    
    var unhideMultipleChoice = () => { 
        addButton.classList.remove('hide');
        multipleChoiceContainer.classList.remove('hide');
    }
    
    var hideShortAnswer = () => { 
        inputShort.classList.add('hide');
        addButton.classList.add('hide');
    }
    
    var unhideShortAnswer = () => { 
        inputShort.classList.remove('hide');
        addButton.classList.remove('hide');
    }
    
    var hideTrueOrFalse = () => { 
        inputTrue.classList.add('hide');
        inputFalse.classList.add('hide');
        trueFalseContainer.classList.add('hide');
        addButton.classList.add('hide');
    }
    
    var unhideTrueOrFalse = () => { 
        inputTrue.classList.remove('hide');
        inputFalse.classList.remove('hide');
        trueFalseContainer.classList.remove('hide');
        addButton.classList.remove('hide');
    }
    
    var hideQuestion = () => {
        questionContainer.classList.add('hide');
    }

    var unhideQuestion = () => {
        questionContainer.classList.remove('hide');
    }
    
    var showSuccess = () => {
        successText.classList.remove('hide');
        scoreText.innerHTML = 'Your score was: ' + score + '/' + totalMC
        scoreText.classList.remove('hide');
        disclaimer.classList.remove('hide');
    }

}

