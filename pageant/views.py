from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect

from django.views.decorators.csrf import requires_csrf_token
from pageant.models import Pageant, CriteriaCategory, Criteria, ParticipantGroup, PageantParticipant, Judge, PageantParticipantRating

from django.db.models import Avg, Sum

# Create your views here.
@login_required(login_url='/login')
def pageant(request, pageant_id):
    pageant_details = get_object_or_404(Pageant, pk=pageant_id)
    category_list_main = []
    group_list = []
    participant_list = []
    categories = CriteriaCategory.objects.filter(pageant=pageant_details)
    groups = ParticipantGroup.objects.filter(pageant=pageant_details)
    overall_rank = [[] for i in range(3)]
    overall = []
    template = ''

    for category in categories:
        category_list_main.append({'detail': category, 'criteria': Criteria.objects.filter(category=category)})

    for group in groups:        
        category_list = []
        overall_rank = []
        overall = []
        for category in categories:
            criterias = Criteria.objects.filter(category=category)
            participant_list = []
            for idx, participant in enumerate(PageantParticipant.objects.filter(group=group)):
                rating_list = []
                total = 0
                for criteria in criterias:
                    try:
                        judge = Judge.objects.get(user=request.user,pageant=pageant_details)
                        try:
                            rating_query = PageantParticipantRating.objects.get(judge=judge, criteria=criteria, participant=participant)
                            rating = rating_query.rating
                        except:
                            rating = ''
                        template = 'pageant_details.html'
                    except:
                            rating_query = PageantParticipantRating.objects.filter(criteria=criteria, participant=participant).aggregate(Avg('rating'))
                            rating = rating_query["rating__avg"]
                            template = 'pageant_details_open.html'
                    try:
                        total = total + rating
                    except:
                        pass
                    rating_list.append({'score': rating, 'max': criteria.maximum_score, 'id': criteria.id})
                participant_list.append({'detail': participant, 'rating' : rating_list, 'total': total})
                try:
                    overall_rank[idx].append(total)
                except:
                    overall_rank.append([total])
            category_list.append({'detail': category, 'participants' : participant_list})
        for idx, participant in enumerate(PageantParticipant.objects.filter(group=group)):
            participant_scores = []
            total = 0
            for indx in range(len(categories)):
                participant_scores.append({'score' : overall_rank[idx][indx], 'percentage' : (overall_rank[idx][indx]/100)*categories[indx].weight })
                total = total + (overall_rank[idx][indx]/100)*categories[indx].weight
            overall.append({'detail':participant, 'scores':participant_scores, 'total': total})
        group_list.append({'detail': group, 'categories': category_list, 'overall' : overall})

    details = {'details': pageant_details, 'categories' : category_list_main, 'groups' : group_list}
    # print template
    return render_to_response(template, details, context_instance=RequestContext(request))

@login_required(login_url='/login')
def all_ratings(request, pageant_id,group_id):
    pageant_details = get_object_or_404(Pageant, pk=pageant_id)
    category_list_main = []
    group_list = []
    participant_list = []
    categories = CriteriaCategory.objects.filter(pageant=pageant_details)
    groups = ParticipantGroup.objects.filter(pageant=pageant_details, pk=group_id)
    overall_rank = [[] for i in range(3)]
    overall = []
    judges = Judge.objects.filter(pageant=pageant_details)

    for category in categories:
        category_list_main.append({'detail': category, 'criteria': Criteria.objects.filter(category=category)})

    for group in groups:        
        category_list = []
        overall_rank = []
        overall = []
        for cat_idx,category in enumerate(categories):
            criterias = Criteria.objects.filter(category=category)
            participant_list = []

            for idx, participant in enumerate(PageantParticipant.objects.filter(group=group)):
                rating_list = []
                totals = []
                participant_gt = 0

                for criteria in criterias:
                    judge_rating = []
                    for judge_row in judges:
                        try:
                            rating_query = PageantParticipantRating.objects.get(judge= judge_row, criteria=criteria, participant=participant)
                            rating = rating_query.rating
                        except:
                            rating = ''
                        judge_rating.append(rating)
                        
                    ratings_count = len(PageantParticipantRating.objects.filter(criteria=criteria, participant=participant))

                    try:
                        rating_query = PageantParticipantRating.objects.filter(criteria=criteria, participant=participant).aggregate(Sum('rating'))
                        #participant_average = rating_query['rating__sum']/len(judges)
                        participant_average = rating_query['rating__sum']/ratings_count
                    except:
                        participant_average = 0

                    rating_list.append({'scores': judge_rating, 'pt_average': participant_average})
                
                for  judge_row in judges:
                    participant_total = 0
                    try:
                        rating_query = PageantParticipantRating.objects.filter(judge=judge_row, participant=participant, criteria__category=category).aggregate(Sum('rating'))
                        participant_total = rating_query['rating__sum']
                        participant_gt = participant_gt + participant_total                        
                    except:
                        participant_total = 0
                        participant_gt = participant_gt + participant_total
                    totals.append(participant_total)
                    
                #if category.id == 1:
                #    participant_list.append({'detail': participant, 'rating' : rating_list, 'totals': totals, 'participant_gt' : participant_gt/(len(judges)-1)})
                #else:
                participant_list.append({'detail': participant, 'rating' : rating_list, 'totals': totals, 'participant_gt' : participant_gt/len(judges)})
                
 
                try:
                    #if category.id == 1:
                    #    overall_rank[idx].append( participant_gt/(len(judges)-1))
                    #else:
                    overall_rank[idx].append( participant_gt/len(judges))
                except:
                    #if category.id == 1:
                    #    overall_rank.append([participant_gt/(len(judges)-1)])
                    #else:
                    overall_rank.append([participant_gt/len(judges)])

            category_list.append({'detail': category, 'participants' : participant_list})

        for idx, participant in enumerate(PageantParticipant.objects.filter(group=group)):
            participant_scores = []
            total = 0
            for indx in range(len(categories)):
                participant_scores.append({'score' : overall_rank[idx][indx], 'percentage' : (overall_rank[idx][indx]/100)*categories[indx].weight })
                total = total + (overall_rank[idx][indx]/100)*categories[indx].weight
            overall.append({'detail':participant, 'scores':participant_scores, 'total': total})
        #print overall
        group_list.append({'detail': group, 'categories': category_list, 'overall' : overall})


    details = {'details': pageant_details, 'categories' : category_list_main, 'groups' : group_list, 'judges': judges}
    return render_to_response('pageant_details_overall.html', details, context_instance=RequestContext(request))
    
def pageant_process(request, pageant_id):
    rating_get = lambda *keys: request.POST['-'.join(['%s' % str(key) for key in keys])]
    pageant_details = get_object_or_404(Pageant, pk=pageant_id)
    categories = CriteriaCategory.objects.filter(pageant__pk=pageant_id)
    #categories = CriteriaCategory.objects.filter(pageant=pageant_details)
    groups = ParticipantGroup.objects.filter(pageant__pk=pageant_id)

    for group in groups:
        participants = PageantParticipant.objects.filter(group=group)
        for participant in participants:
            for category in categories:
                criterias = Criteria.objects.filter(category=category)
                for criteria in criterias:
                    judge_rating = Judge.objects.get(user=request.user,pageant=pageant_details)
                    participant_rating,created = PageantParticipantRating.objects.get_or_create(criteria=criteria, participant=participant, judge=judge_rating)
                    if request.POST.get(str(participant.id)+'-'+str(criteria.id)) == '' or request.POST.get(str(participant.id)+'-'+str(criteria.id)) is None:
                        pass
                    else:
                        participant_rating.rating = request.POST.get(str(participant.id)+'-'+str(criteria.id))
                        if participant_rating.rating == None:
                            pass
                        else:
                            participant_rating.save()
    #return render_to_response('login.html', {}, context_instance=RequestContext(request))
    messages.success(request, "Ratings has been saved.")
    return HttpResponseRedirect('/pageant/'+pageant_id)

@login_required(login_url='/login')
def print_ratings(request, pageant_id, group_id):
   pageant_details = get_object_or_404(Pageant, pk=pageant_id)
   category_list_main = []
   group_list = []
   participant_list = []
   categories = CriteriaCategory.objects.filter(pageant=pageant_details)
   groups = ParticipantGroup.objects.filter(pageant=pageant_details, pk=group_id)
   overall_rank = [[] for i in range(3)]
   overall = []
   judges = Judge.objects.filter(pageant=pageant_details)

   for category in categories:
      category_list_main.append({'detail': category, 'criteria': Criteria.objects.filter(category=category)})

   for group in groups:        
      category_list = []
      overall_rank = []
      overall = []
      for cat_idx,category in enumerate(categories):
         criterias = Criteria.objects.filter(category=category)
         participant_list = []

         for idx, participant in enumerate(PageantParticipant.objects.filter(group=group)):
               rating_list = []
               totals = []
               participant_gt = 0

               for criteria in criterias:
                  judge_rating = []
                  for judge_row in judges:
                     try:
                           rating_query = PageantParticipantRating.objects.get(judge= judge_row, criteria=criteria, participant=participant)
                           rating = rating_query.rating
                     except:
                           rating = ''
                     judge_rating.append(rating)
                     
                  ratings_count = len(PageantParticipantRating.objects.filter(criteria=criteria, participant=participant))

                  try:
                     rating_query = PageantParticipantRating.objects.filter(criteria=criteria, participant=participant).aggregate(Sum('rating'))
                     #participant_average = rating_query['rating__sum']/len(judges)
                     participant_average = rating_query['rating__sum']/ratings_count
                  except:
                     participant_average = 0

                  rating_list.append({'scores': judge_rating, 'pt_average': participant_average})
               
               for  judge_row in judges:
                  participant_total = 0
                  try:
                     rating_query = PageantParticipantRating.objects.filter(judge=judge_row, participant=participant, criteria__category=category).aggregate(Sum('rating'))
                     participant_total = rating_query['rating__sum']
                     participant_gt = participant_gt + participant_total                    
                  except:
                     participant_total = 0
                     participant_gt = participant_gt + participant_total
                  totals.append(participant_total)
                  
               #if category.id == 1:
               #    participant_list.append({'detail': participant, 'rating' : rating_list, 'totals': totals, 'participant_gt' : participant_gt/(len(judges)-1)})
               #else:
               participant_list.append({'detail': participant, 'rating' : rating_list, 'totals': totals, 'participant_gt' : participant_gt/len(judges)-participant.deduction})

               try:
                  #if category.id == 1:
                  #    overall_rank[idx].append( participant_gt/(len(judges)-1))
                  #else:
                  overall_rank[idx].append( participant_gt/len(judges))
               except:
                  #if category.id == 1:
                  #    overall_rank.append([participant_gt/(len(judges)-1)])
                  #else:
                  overall_rank.append([participant_gt/len(judges)])


         category_list.append({'detail': category, 'participants' : participant_list})

      for idx, participant in enumerate(PageantParticipant.objects.filter(group=group)):
         participant_scores = []
         total = 0
         for indx in range(len(categories)):
               participant_scores.append({'score' : overall_rank[idx][indx], 'percentage' : (overall_rank[idx][indx]/100)*categories[indx].weight })
               total = total + (overall_rank[idx][indx]/100)*categories[indx].weight
         overall.append({'detail':participant, 'scores':participant_scores, 'total': total})
      #print overall
      group_list.append({'detail': group, 'categories': category_list, 'overall' : overall})


   details = {'details': pageant_details, 'categories' : category_list_main, 'groups' : group_list, 'judges': judges}
   return render_to_response('print_score.html', details, context_instance=RequestContext(request))