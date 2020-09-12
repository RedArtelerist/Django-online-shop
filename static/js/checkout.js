/* ----------------------------
	CustomValidation prototype
	- Keeps track of the list of invalidity messages for this input
	- Keeps track of what validity checks need to be performed for this input
	- Performs the validity checks and sends feedback to the front end
---------------------------- */

function CustomValidation(input) {
	this.invalidities = [];
	this.validityChecks = [];

	//add reference to the input node
	this.inputNode = input;

	//trigger method to attach the listener
	this.registerListener();
}

CustomValidation.prototype = {
	addInvalidity: function (message) {
		this.invalidities.push(message);
	},
	getInvalidities: function () {
		return this.invalidities.join('. \n');
	},
	checkValidity: function (input) {
		for (var i = 0; i < this.validityChecks.length; i++) {

			var isInvalid = this.validityChecks[i].isInvalid(input);
			if (isInvalid) {
				this.addInvalidity(this.validityChecks[i].invalidityMessage);
			}

			var requirementElement = this.validityChecks[i].element;

			if (requirementElement) {
				if (isInvalid) {
					requirementElement.classList.add('invalid');
					requirementElement.classList.remove('valid');
				} else {
					requirementElement.classList.remove('invalid');
					requirementElement.classList.add('valid');
				}

			} // end if requirementElement
		} // end for
	},
	checkInput: function () { // checkInput now encapsulated

		this.inputNode.CustomValidation.invalidities = [];
		this.checkValidity(this.inputNode);

		if (this.inputNode.CustomValidation.invalidities.length === 0 && this.inputNode.value !== '') {
			this.inputNode.setCustomValidity('');
		} else {
			var message = this.inputNode.CustomValidation.getInvalidities();
			this.inputNode.setCustomValidity(message);
		}
	},
	registerListener: function () { //register the listener here

		var CustomValidation = this;

		this.inputNode.addEventListener('keyup', function () {
			CustomValidation.checkInput();
		});
	}

};

/* ----------------------------
	Validity Checks
	The arrays of validity checks for each input
	Comprised of three things
		1. isInvalid() - the function to determine if the input fulfills a particular requirement
		2. invalidityMessage - the error message to display if the field is invalid
		3. element - The element that states the requirement
---------------------------- */

var userNameValidityChecks = [
	{
		isInvalid: function (input) {
			return input.value.length == 0;
		},
		invalidityMessage: 'Required',
		element: document.querySelector('label[for="userName"] .input-requirements li:nth-child(1)')
	},
	{
		isInvalid: function (input) {
			return (input.value.length < 5 || input.value.length > 20);
		},
		invalidityMessage: 'This input needs to be at least 5 characters and at maximum 20',
		element: document.querySelector('label[for="userName"] .input-requirements li:nth-child(2)')
	},
	{
		isInvalid: function (input) {
			var illegalCharacters = input.value.match(/[^a-zA-Z0-9.\s-_]/g);
			return illegalCharacters ? true : false;
		},
		invalidityMessage: 'Only letters are allowed',
		element: document.querySelector('label[for="userName"] .input-requirements li:nth-child(3)')
	}
];


var countryNameValidityChecks = [
	{
		isInvalid: function (input) {
			return input.value.length == 0;
		},
		invalidityMessage: 'Required',
		element: document.querySelector('label[for="country"] .input-requirements li:nth-child(1)')
	},
	{
		isInvalid: function (input) {
			return (input.value.length < 3 || input.value.length > 30);
		},
		invalidityMessage: 'This input needs to be at least 3 characters and at maximum 30',
		element: document.querySelector('label[for="country"] .input-requirements li:nth-child(2)')
	},
	{
		isInvalid: function (input) {
			var illegalCharacters = input.value.match(/[^a-zA-Z\s-]/g);
			return illegalCharacters ? true : false;
		},
		invalidityMessage: 'Only letters are allowed',
		element: document.querySelector('label[for="country"] .input-requirements li:nth-child(3)')
	}
];

var cityNameValidityChecks = [
	{
		isInvalid: function (input) {
			return input.value.length == 0;
		},
		invalidityMessage: 'Required',
		element: document.querySelector('label[for="city"] .input-requirements li:nth-child(1)')
	},
	{
		isInvalid: function (input) {
			return (input.value.length < 3 || input.value.length > 30);
		},
		invalidityMessage: 'This input needs to be at least 3 characters and at maximum 30',
		element: document.querySelector('label[for="city"] .input-requirements li:nth-child(2)')
	},
	{
		isInvalid: function (input) {
			var illegalCharacters = input.value.match(/[^a-zA-Z\s-]/g);
			return illegalCharacters ? true : false;
		},
		invalidityMessage: 'Only letters are allowed',
		element: document.querySelector('label[for="city"] .input-requirements li:nth-child(3)')
	}
];


var stateNameValidityChecks = [
	{
		isInvalid: function (input) {
			return input.value.length == 0;
		},
		invalidityMessage: 'Required',
		element: document.querySelector('label[for="state"] .input-requirements li:nth-child(1)')
	},
	{
		isInvalid: function (input) {
			return (input.value.length < 3 || input.value.length > 30);
		},
		invalidityMessage: 'This input needs to be at least 3 characters and at maximum 30',
		element: document.querySelector('label[for="state"] .input-requirements li:nth-child(2)')
	},
	{
		isInvalid: function (input) {
			var illegalCharacters = input.value.match(/[^a-zA-Z\s-]/g);
			return illegalCharacters ? true : false;
		},
		invalidityMessage: 'Only letters are allowed',
		element: document.querySelector('label[for="state"] .input-requirements li:nth-child(3)')
	}
];



var addressNameValidityChecks = [
	{
		isInvalid: function (input) {
			return input.value.length == 0;
		},
		invalidityMessage: 'Required',
		element: document.querySelector('label[for="address"] .input-requirements li:nth-child(1)')
	},
	{
		isInvalid: function (input) {
			return (input.value.length < 3 || input.value.length > 50);
		},
		invalidityMessage: 'This input needs to be at least 3 characters and at maximum 50',
		element: document.querySelector('label[for="address"] .input-requirements li:nth-child(2)')
	},
	{
		isInvalid: function (input) {
			var illegalCharacters = input.value.match(/[^a-zA-Z0-9\s-\/]/g);
			return illegalCharacters ? true : false;
		},
		invalidityMessage: 'Only letters and digits are allowed',
		element: document.querySelector('label[for="address"] .input-requirements li:nth-child(3)')
	}
];


var zipcodeNameValidityChecks = [
	{
		isInvalid: function (input) {
			return input.value.length == 0;
		},
		invalidityMessage: 'Required',
		element: document.querySelector('label[for="zipcode"] .input-requirements li:nth-child(1)')
	},
	{
		isInvalid: function (input) {
			//[(^\d{5}$)|(^\d{5}-\d{4}$)]
			var illegalCharacters = input.value.match(/(^\d{5}$)|(^\d{5}-\d{4}$)/g);
			return illegalCharacters ? false : true;
		},
		invalidityMessage: 'Only 5 digits are allowed',
		element: document.querySelector('label[for="zipcode"] .input-requirements li:nth-child(2)')
	}
];

/* ----------------------------
	Setup CustomValidation
	Setup the CustomValidation prototype for each input
	Also sets which array of validity checks to use for that input
---------------------------- */

if (user == 'AnonymousUser'){
	var userNameInput = document.getElementById('userName');
	userNameInput.CustomValidation = new CustomValidation(userNameInput);
	userNameInput.CustomValidation.validityChecks = userNameValidityChecks;
}

var countryNameInput = document.getElementById('country');
var stateNameInput = document.getElementById('state');
var cityNameInput = document.getElementById('city');
var addressNameInput = document.getElementById('address');
var zipcodeNameInput = document.getElementById('zipcode');


countryNameInput.CustomValidation = new CustomValidation(countryNameInput);
countryNameInput.CustomValidation.validityChecks = countryNameValidityChecks;

stateNameInput.CustomValidation = new CustomValidation(stateNameInput);
stateNameInput.CustomValidation.validityChecks = stateNameValidityChecks;

cityNameInput.CustomValidation = new CustomValidation(cityNameInput);
cityNameInput.CustomValidation.validityChecks = cityNameValidityChecks;

addressNameInput.CustomValidation = new CustomValidation(addressNameInput);
addressNameInput.CustomValidation.validityChecks = addressNameValidityChecks;

zipcodeNameInput.CustomValidation = new CustomValidation(zipcodeNameInput);
zipcodeNameInput.CustomValidation.validityChecks = zipcodeNameValidityChecks;


/* ----------------------------
	Event Listeners
---------------------------- */

var inputs = document.querySelectorAll('input:not([type="submit"])');

var submit = document.querySelector('input[type="submit"]');
var form = document.getElementById('form');

function validate() {
	for (var i = 0; i < inputs.length; i++) {
		inputs[i].CustomValidation.checkInput();
	}
}

submit.addEventListener('click', validate);
form.addEventListener('submit', validate);
