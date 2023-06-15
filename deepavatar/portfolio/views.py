import os
from django.shortcuts import render
from django.contrib import messages
import pandas as pd
from .models import (
		UserProfile,
		Projects,
		Certificate,
		AvatarFeed,
		Skill
	)
from django.views import generic
from django.http import JsonResponse, StreamingHttpResponse
from .forms import ContactForm
from .utils import chat, avatar_gen, ScriptFinder, generate_presigned_url


video_paths = [
    "1.mp4",
    "2.mp4",
    "3.mp4",
    "4.mp4",
    "5.mp4",
    "6.mp4",
    "7.mp4",
    "8.mp4",
    "9.mp4",
    "10.mp4",
    "11.mp4",
    "12.mp4",
    "13.mp4",
    "14.mp4",
    "15.mp4",
    "16.mp4",
    "17.mp4",
    "18.mp4",
    "19.mp4",
    "20.mp4",
    "21.mp4",
    "22.mp4",
    "23.mp4",
    "24.mp4",
    "25.mp4",
    "26.mp4",
    "27.mp4",
    "28.mp4"
]


def start_avatar_chat_to_user(request):
	if request.method == "POST":
		the_feed = AvatarFeed()
		the_feed.user_question_message = "None"
		the_feed.video_path = "None"
		the_feed.video_changed = "False"
		the_feed.first_video = "False"
		the_feed.save()
		the_feed_object_id = str(the_feed.pk)

		response = {
			'the_feed_object_id': the_feed_object_id 
		}

		return JsonResponse(response)

def check_for_new_posted_video(request):
	if request.method == "POST":
		feed_object_id = request.POST.get("feed_object_id", None)
		
		if feed_object_id != "OFF":
			the_feed = AvatarFeed.objects.filter(pk=feed_object_id).first()
			video_changed = the_feed.video_changed
			first_video = the_feed.first_video
			# print("video_changed")
			# print(video_changed)
			# print("first_video")
			# print(first_video)

			if video_changed == "True":
				new_video = "True"
				video_path = the_feed.video_path
				the_feed.video_changed = "False"
				the_feed.save(update_fields=["video_changed"])
				video_path = generate_presigned_url(video_path)
			else:
				new_video = "False"
				video_path = "None"
		else:
			new_video = "False"
			first_video = "False"
			video_path = "None"

		response = {
			'new_video': new_video,
			'first_video': first_video,
			'video_path': video_path,
		}

		return JsonResponse(response)

def get_avatar_response(request):
	if request.method == "POST":
		user_question_text = request.POST.get("user_question_text", None)
		feed_object_id = request.POST.get("feed_object_id", None)
		started_asking_questions = request.POST.get("started_asking_questions", None)

		the_feed = AvatarFeed.objects.filter(pk=feed_object_id).first()
		the_feed_object_id = feed_object_id
		curr_user_question_message = the_feed.user_question_message
		the_feed.user_question_message = user_question_text
		the_feed.save(update_fields=["user_question_message"])

		# First Question!
		#scripts_path = os.path.join(os.getcwd(), "Scripts.xlsx")
		scripts_path = "/mnt/avatar_storage/Scripts.xlsx"
		embedded_scripts_path = "/mnt/avatar_storage/Scripts_embedding.csv"
		script_finder = ScriptFinder(embedded_scripts_path)

		#script_finder.generate_embeddings_from_scripts()
		
		the_feed = AvatarFeed.objects.filter(pk=the_feed_object_id).first()
		new_user_question_message = the_feed.user_question_message

		# if new_user_question_message != curr_user_question_message:
		# 	curr_user_question_message = new_user_question_message

		# 	video_path = video_paths[new_user_question_message]
			
		# 	the_feed.video_path = video_path
		# 	the_feed.video_changed = "True"
		# 	the_feed.first_video = "False"
		# 	the_feed.save(update_fields=["video_path", "video_changed", "first_video"])
		# elif first_question == True:
		# 	first_question = False

		# 	video_path = video_paths[new_user_question_message]
			
		# 	the_feed.video_path = video_path
		# 	the_feed.video_changed = "True"
		# 	the_feed.first_video = "True"
		# 	the_feed.save(update_fields=["video_path", "video_changed", "first_video"])

		if new_user_question_message != curr_user_question_message:
			curr_user_question_message = new_user_question_message
			model_response = chat(curr_user_question_message)

			# script_finder.df = pd.read_csv(embedded_scripts_path)
			
			query_results = script_finder.find_similar_text(model_response)
			video_path = query_results.iloc[0]["video_path"]
			the_feed.video_path = video_path
			the_feed.video_changed = "True"
			the_feed.first_video = "False"
			the_feed.save(update_fields=["video_path", "video_changed", "first_video"])
		# elif first_question == True:
		# 	first_question = False
		# 	model_response = chat(curr_user_question_message)
			
		# 	query_results = script_finder.find_similar_text(model_response)
		# 	video_path = query_results.iloc[0]["video_path"]
		# 	the_feed.video_path = video_path
		# 	the_feed.video_changed = "True"
		# 	the_feed.first_video = "True"
		# 	the_feed.save(update_fields=["video_path", "video_changed", "first_video"])
		
		response = {
			'msg': "success"
		}

		return JsonResponse(response)

		# if started_asking_questions == "False":
		# 	# First Question!
		# 	#scripts_path = os.path.join(os.getcwd(), "Scripts.xlsx")
		# 	scripts_path = "/mnt/avatar_storage/Scripts.xlsx"
		# 	script_finder = ScriptFinder(scripts_path)
		# 	script_finder.generate_embeddings_from_scripts()

		# 	curr_user_question_message = user_question_text
		# 	first_question = True

		# 	while(True):
		# 		the_feed = AvatarFeed.objects.filter(pk=the_feed_object_id).first()
		# 		new_user_question_message = the_feed.user_question_message

		# 		# if new_user_question_message != curr_user_question_message:
		# 		# 	curr_user_question_message = new_user_question_message

		# 		# 	video_path = video_paths[new_user_question_message]
					
		# 		# 	the_feed.video_path = video_path
		# 		# 	the_feed.video_changed = "True"
		# 		# 	the_feed.first_video = "False"
		# 		# 	the_feed.save(update_fields=["video_path", "video_changed", "first_video"])
		# 		# elif first_question == True:
		# 		# 	first_question = False

		# 		# 	video_path = video_paths[new_user_question_message]
					
		# 		# 	the_feed.video_path = video_path
		# 		# 	the_feed.video_changed = "True"
		# 		# 	the_feed.first_video = "True"
		# 		# 	the_feed.save(update_fields=["video_path", "video_changed", "first_video"])

		# 		if new_user_question_message != curr_user_question_message:
		# 			curr_user_question_message = new_user_question_message
		# 			model_response = chat(curr_user_question_message)
					
		# 			query_results = script_finder.find_similar_text(model_response)
		# 			video_path = query_results.iloc[0]["video_path"]
		# 			the_feed.video_path = video_path
		# 			the_feed.video_changed = "True"
		# 			the_feed.first_video = "False"
		# 			the_feed.save(update_fields=["video_path", "video_changed", "first_video"])
		# 		elif first_question == True:
		# 			first_question = False
		# 			model_response = chat(curr_user_question_message)
					
		# 			query_results = script_finder.find_similar_text(model_response)
		# 			video_path = query_results.iloc[0]["video_path"]
		# 			the_feed.video_path = video_path
		# 			the_feed.video_changed = "True"
		# 			the_feed.first_video = "True"
		# 			the_feed.save(update_fields=["video_path", "video_changed", "first_video"])
		
		# response = {
		# 	'msg': "success"
		# }

		# return JsonResponse(response)

def update_avatar_feed(request, video_path=""):
	return StreamingHttpResponse(avatar_gen(video_path), content_type='multipart/x-mixed-replace; boundary=frame')

class IndexView(generic.TemplateView):
	template_name = "portfolio/index.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		certificates = Certificate.objects.filter(is_active=True)
		projects = Projects.objects.filter(is_active=True)
		skills = Skill.objects.all()
		
		context["certificates"] = certificates
		context["projects"] = projects
		context["skills"] = skills
		return context

class ContactView(generic.FormView):
	template_name = "portfolio/contact.html"
	form_class = ContactForm
	success_url = "/"
	
	def form_valid(self, form):
		form.save()
		messages.success(self.request, 'Thank you. We will be in touch soon.')
		return super().form_valid(form)

class ProjectsView(generic.ListView):
	model = Projects
	template_name = "portfolio/projects.html"
	paginate_by = 10

	def get_queryset(self):
		return super().get_queryset().filter(is_active=True)

class ProjectsDetailView(generic.DetailView):
	model = Projects
	template_name = "portfolio/projects-detail.html"