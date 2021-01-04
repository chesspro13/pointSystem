from django.http import HttpResponse
from django.shortcuts import render

from pages.forms import PointSubmissionForm
from chores.models import basic_chore
from pointRequests.models import pointRequest
from django.shortcuts import redirect

from datetime import date

from people.models import Brandon
from people.models import Jennifer
from people.models import Pandora
from people.models import Violet

from people.models import invalid_passwords

name = ''
task = ''

def home_page(request, *args, **kwargs):
	k = basic_chore.objects.all()

	for i in k:
	    print('===' + i.name.replace('&&',' ') + '===')
	    print('----')
	    print('Description: ' + i.description)
	    print('<br>')
	    print('Requirements: ' + i.requirements)
	    print('<br>')
	    print('Limitations: ' + i.limitations)
	    print('<br>')
	    print('Point Values: ' + str(i.pointValue))
	    print('')
	return render(request, "index.html", {})


def point_submission( request, *args, **kwargs):
	form = PointSubmissionForm(request.POST or None)

	#print( type(form.fields['chore'].widget.choices))

	#form.fields['chore'].widget.choices['butt': 'whole']

	#print( (form.fields['chore'].widget.choices))
	#form.fields['chore'].choices = []
#	print(form.fields['chore'].choices)
	choices = []
	for i in basic_chore.objects.all():
		print( i.name.replace('&&','&nbsp;') )


		form.fields['chore'].widget.choices.append( ( i.name.replace('&&','_'),i.name.replace('&&','_') ) )


	if form.is_valid():
		form.save()
		form = PointSubmissionForm()
	context = {
		'form': form
	}

	return render(request, "point_submission_page.html", context)

def request_submitted( request,*args, **kwargs):
	context = {
		'person' : request.POST['name'],
		'chore' : request.POST['chore'],
		'date' : date.today().strftime('%d-%b-%y')
	}

	pr = pointRequest(name=context['person'],chore=context['chore'], date=date.today().strftime('%d-%b-%y'))
	pr.save()

	return render(request, 'request_submitted.html', context)

def pending_requests( request, *args, **kwargs):
	global name
	global task

	pendingRequests = []

	for i in pointRequest.objects.all():
		pendingRequests.append((i.name, i.chore, i.date))



	context = {
		'rl': pendingRequests
	}
	
	return render(request, 'pending_requests.html', context)

def review_task( request, *args, **kwargs):
	print( 'reviewing for ' + request.POST.get('Name'))
	context = {
		'name' : request.POST.get('Name'),
		'task' : request.POST.get('Task'),
		'date' : request.POST.get('Dask'),

	}
	return render(request, 'review_task.html', context)

def result(request, *args, **kwargs):

	output = ['Name: '+ request.POST.get('Name'), 'Task: '+ request.POST.get("Task")]


	print('task ' + request.POST.get("Task"))

	if request.POST.get('shittyPassword') != '':
		k = invalid_passwords(name=request.POST.get('Name'), task=request.POST.get('Task'),date=date.today().strftime('%d-%b-%y'))
		k.save()
		return redirect('invalid_password/')

	for i, k in request.POST.items():

		if 'approved' in i:
			print("Yay! It has been approved!")
			output.append('Status: Approved')
			context = {
				'output': output
			}
			addTaskToDB( request.POST.get('Name'), request.POST.get('Task'), request.POST.get('Unprompted'), request.POST.get('Notes'), int( request.POST.get('PointAdjustment')), request.POST.get('Date') )

		if 'denied' in i:
			print("Fuck! It wasn't approved!")
			output.append('Status: Denied')
			context = {
				'output': output
			}
			##addRemarkToDB( request.POST.get('Name'), request.POST.get('Task'), request.POST.get('Notes') )
			print("Action removec")

	return render(request, 'result.html', context)

def view_points(request, *args, **kwargs):


	items = getDataFromDatabase( request.POST.get('Name') )

	context = {
		'name': request.POST.get('Name'),
		'output': items[0],
		'points': items[1]
	}


	return render(request, 'view_points.html', context)

def invalid_password_warning(request, *args, **kwargs):
	return render(request, 'invalid_password.html', {})

def lapse_of_judgement(request, *args, **kwargs):

	items = []

	for i in invalid_passwords.objects.all():
		items.append((i.date, i.name, i.task))


	context = {
		'output': items
	}
	return render(request, 'lapse_of_judgement.html', context)


















def addTaskToDB( name, task, unprompted, notes, pointAdjustment, dateOfChore):
	k = list(basic_chore.objects.all())
	points = pointAdjustment

	remarks = notes
	newShit = None

	for i in k:
		if i.name.replace('&&','_') == task:
			print('Points: ' + str(type( points)))
			print( 'PointValue ' + str(type(i.pointValue)))
			points = points + i.pointValue
			print( 'Total points: ' + str( points))

	if unprompted:
		if( notes == ''):
			remarks = 'Unprompted'
		else:
			remarks = 'Unprompted/' + notes
		
		points = points + 5


	print(name)

	if name == 'Brandon':
		newShit = Brandon(date=dateOfChore, task=task, remarks=remarks, points=points)


	if name == 'Jennifer':
		newShit = Jennifer(date=dateOfChore, task=task, remarks=remarks, points=points)


	if name == 'Pandora':
		newShit = Pandora(date=dateOfChore, task=task, remarks=remarks, points=points)


	if name == 'Violet':
		newShit = Violet(date=dateOfChore, task=task, remarks=remarks, points=points)



	for i in pointRequest.objects.all():
		if i.name == name and i.chore == task.replace('&&','_') and i.date == dateOfChore:
			#pointRequest.objects.filter(id=i.id).delete()
			print("Task removed from pending and is now submitted.")
			newShit.save()
			return 

	print("Failed to add to database!")

def addRemarkToDB( name, task ):
	if name == 'Brandon':
		newShit = Brandon(date='Today', task=task, remarks='Nope. Not done right.', points='0')
	if name == 'Jennifer':
		newShit = Brandon(date='Today', task=task, remarks='Nope. Not done right.', points='0')
	if name == 'Pandora':
		newShit = Brandon(date='Today', task=task, remarks='Nope. Not done right.', points='0')
	if name == 'Violet':
		newShit = Brandon(date='Today', task=task, remarks='Nope. Not done right.', points='0')

	newShit.save()

def getDataFromDatabase( name ):
	points = 0
	if name == 'Brandon':
		li = Brandon.objects.all()
		print( li.count())
		for i in li:
			print( i.date + "  '" + i.task + "'  '" +  i.remarks + "'  " + str(i.points) )
			points += i.points

		#print( 'returning ' + type(li) + ' items for brandon')
		return (li, points)

	points = 0
	if name == 'Jennifer':
		li = Jennifer.objects.all()
		print( li.count())
		for i in li:
			print( i.date + "  '" + i.task + "'  '" +  i.remarks + "'  " + str(i.points) )
			points += i.points

		#print( 'returning ' + type(li) + ' items for brandon')
		return (li, points)

	points = 0
	if name == 'Pandora':
		li = Pandora.objects.all()
		print( li.count())
		for i in li:
			print( i.date + "  '" + i.task + "'  '" +  i.remarks + "'  " + str(i.points) )
			points += i.points

		#print( 'returning ' + type(li) + ' items for brandon')
		return (li, points)

	points = 0
	if name == 'Violet':
		li = Violet.objects.all()
		print( li.count())
		for i in li:
			print( i.date + "  '" + i.task + "'  '" +  i.remarks + "'  " + str(i.points) )
			points += i.points

		#print( 'returning ' + type(li) + ' items for brandon')
		return (li, points)