//dashboard nav highlight
function changeNav(id) {
	document.getElementById(id).classList.remove('btn-outline-info')
	document.getElementById(id).classList.add('btn-info')
}

function toggleForm(id) {
	viewclass = id.concat('-view')
	editclass = id.concat('-edit')
	checkid = id.concat('-check')

	check = document.getElementById(checkid)
	views = document.getElementsByClassName(viewclass)
	fields = document.getElementsByClassName(editclass)


	if (check.checked) {
		for (let i = 0; i < views.length; i++) {
  			fields[i].classList.remove('d-none')
  			views[i].classList.add('d-none')
		}	
	}
	else {
		for (let i = 0; i < views.length; i++) {
  			fields[i].classList.add('d-none')
  			views[i].classList.remove('d-none')
		}
	}
	
}
function doAlert() {
	alert('working')
}

 
//dashboard nav toggle
