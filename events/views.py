from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import Http404

from django.views.decorators.csrf import requires_csrf_token

from django.db.models import Avg
from events.models import Event, Criteria, Participant, ParticipantRating, Judge
from pageant.models import Pageant

def is_users_event(request, event_id):
    if not request.user.is_anonymous():
        user_judge = Judge.objects.filter(user=request.user, event__pk=event_id)
        if user_judge:
            return True
    return False


def home(request):
    events = Event.objects.all().order_by('is_closed', '-id')
    pageants = Pageant.objects.filter(is_closed=False).order_by('is_closed', 'id')
    return render_to_response('index.html', {'events': events, 'pageants': pageants}, context_instance=RequestContext(request))

@requires_csrf_token
def event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404

    participants = Participant.objects.filter(event__pk = event_id).order_by('order')
    criterias = Criteria.objects.filter(event__pk = event_id).order_by('title')

    # Process if items from form is submitted
    if request.method == "POST":
        try:
            participant = Participant.objects.get(pk=request.POST.get("participant"))
            user_judge = Judge.objects.get(event__pk=event_id, user=request.user)
        except Participant.DoesNotExist:
            raise Http404
        
        for criteria in criterias:
            rating, created = ParticipantRating.objects.get_or_create(criteria=criteria, participant=participant, judge=user_judge)
            rating.rating = request.POST.get(str(criteria.id))
            rating.save()
    
    participant_rating = []

    for participant in participants:
        rating = []
        participant_overall = 0
        for criteria in criterias:
            if not is_users_event(request, participant.event.id):
                average_rating = ParticipantRating.objects.filter(participant=participant, criteria=criteria).aggregate(Avg('rating'))
            else:
                average_rating = ParticipantRating.objects.filter(participant=participant, criteria=criteria, judge__user=request.user).aggregate(Avg('rating'))
            if average_rating['rating__avg'] is None:
                rating.append(0)
                participant_overall += 0
            else:
                rating.append((average_rating['rating__avg'],average_rating['rating__avg'] * (criteria.weight/100)))
                participant_overall += average_rating['rating__avg'] * (criteria.weight/100)
        rating.append((participant.deduction, participant_overall-participant.deduction))
        participant_rating.append({'participant': participant, 'rating':rating})

    return render_to_response('event_details.html', {'event': event, 'participants': participant_rating, 'criterias' : criterias}, context_instance=RequestContext(request))

def participant(request, participant_id):
    try:
        participant = Participant.objects.get(pk=participant_id)
    except Participant.DoesNotExist:
        raise Http404

    judge_rating = []
    overall_rating = []
    participant_overall = 0
    criterias2 = criterias = Criteria.objects.filter(event=participant.event)

    if participant.event.is_closed or not is_users_event(request, participant.event.id):
        judges = Judge.objects.filter(event=participant.event)

        # Rating of each judge on the different criterias
        for judge in judges:
            rating = []
            total = 0
            for criteria in criterias:
                criteria_rating = ParticipantRating.objects.filter(participant=participant, criteria=criteria, judge=judge).aggregate(Avg('rating'))
                if criteria_rating['rating__avg'] is None:
                    rating.append(0)
                    total += 0
                else:
                    rating.append(criteria_rating['rating__avg'] * (criteria.weight/100))
                    total += criteria_rating['rating__avg'] * (criteria.weight/100)
            rating.append(participant.deduction)
            rating.append(total-participant.deduction)
            judge_rating.append({'judge': judge, 'rating': rating})

        # Total rating of the participant
        for criteria in criterias2:
            average_rating = ParticipantRating.objects.filter(participant=participant, criteria=criteria).aggregate(Avg('rating'))
            if average_rating['rating__avg'] is None:
                overall_rating.append(0)
                participant_overall += 0
            else:
                overall_rating.append(average_rating['rating__avg'] * (criteria.weight/100))
                participant_overall += average_rating['rating__avg'] * (criteria.weight/100)
        
        overall_rating.append(participant.deduction)
        return render_to_response('participant.html', {'participant': participant, 'event' : participant.event, 'judges' : judge_rating, 'overall_rating' : overall_rating, 'overall_total' : participant_overall-participant.deduction, 'criterias' : criterias}, context_instance=RequestContext(request))
    else:    
        rating = []
        total = 0
        for criteria in criterias:
            criteria_rating = ParticipantRating.objects.filter(participant=participant, criteria=criteria, judge__user=request.user).aggregate(Avg('rating'))
            if criteria_rating['rating__avg'] is None:
                rating.append(0)
                total += 0
            else:
                rating.append(criteria_rating['rating__avg'] * (criteria.weight/100))
                total += criteria_rating['rating__avg'] * (criteria.weight/100)
        rating.append(participant.deduction)
        rating.append(total-participant.deduction)


        return render_to_response('judge.html', {'criterias' : criterias, 'participant' : participant, 'rating' : rating}, context_instance=RequestContext(request))

def raw(request,event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404

    participants = Participant.objects.filter(event__pk = event_id).order_by('order')
    criterias = Criteria.objects.filter(event__pk = event_id).order_by('title')
    judges = Judge.objects.filter(event=event).order_by('user')

    # Process if items from form is submitted
    if request.method == "POST":
        try:
            participant = Participant.objects.get(pk=request.POST.get("participant"))
        except Participant.DoesNotExist:
            raise Http404
        
        for criteria in criterias:
            rating, created = ParticipantRating.objects.get_or_create(criteria=criteria, participant=participant, judge=user_judge)
            rating.rating = request.POST.get(str(criteria.id))
            rating.save()
    
    participant_rating = []

    for participant in participants:
        rating = []
        participant_overall = 0
        judge_ratings = []

        for criteria in criterias:
            average_rating = ParticipantRating.objects.filter(participant=participant, criteria=criteria).aggregate(Avg('rating'))

            if average_rating['rating__avg'] is None:
                rating.append(0)
                participant_overall += 0
            else:
                rating.append((average_rating['rating__avg'],average_rating['rating__avg'] * (criteria.weight/100)))
                participant_overall += average_rating['rating__avg'] * (criteria.weight/100)
        rating.append((participant.deduction, participant_overall-participant.deduction))

        for judge in judges:
            judge_rating = []
            judge_rating_overall = 0

            for criteria in criterias:
                average_rating = ParticipantRating.objects.filter(participant=participant, criteria=criteria, judge=judge).aggregate(Avg('rating'))
                if average_rating['rating__avg'] is None:
                    judge_rating.append(0)
                    judge_rating_overall += 0
                else:
                    judge_rating.append((average_rating['rating__avg'],average_rating['rating__avg'] * (criteria.weight/100)))
                    judge_rating_overall += average_rating['rating__avg'] * (criteria.weight/100)
            judge_rating.append((participant.deduction, judge_rating_overall-participant.deduction))
            judge_ratings.append((judge, judge_rating))

        participant_rating.append({'participant': participant, 'rating':rating, 'judge_rating': judge_ratings, 'overall_rating' : (participant_overall-participant.deduction)})

    # print participant_rating
    participant_rating = sorted(participant_rating, key=lambda k: k['overall_rating'], reverse=True)
    # print participant_rating

    return render_to_response('event_details_raw.html', {'event': event, 'participants': participant_rating, 'criterias' : criterias, 'judges': judges}, context_instance=RequestContext(request))
