import os
import time
import json

# cloudinary for store images
import cloudinary
import cloudinary.uploader
import cloudinary.api

# django imports
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views.generic import RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.serializers.json import DjangoJSONEncoder

# ML imports
import numpy as np
from keras.preprocessing import image
from tensorflow.python.keras.models import model_from_json
from tensorflow.python.keras.initializers import glorot_uniform
from keras.utils import CustomObjectScope
from keras import backend as K

# db table
from .models import UserHistory
# configparser for saving details
from configparser import ConfigParser

# load config file
current_path = os.getcwd()
config_file = os.path.join(current_path, 'config.ini')
config = ConfigParser()
config.read(config_file)

# Configure cloudinary credentials
cloudinary.config(
    cloud_name=config.get("CLOUDINARY", 'cloud_name'),
    api_key=config.get("CLOUDINARY", 'api_key'),
    api_secret=config.get("CLOUDINARY", 'api_secret'),
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AboutPageView(TemplateView):
    """
    class for displaying about page
    """
    template_name = 'about.html'


class HomePageView(TemplateView):
    """
    class for displaying upload page, prediction image and
    upload image in cloudinary
    """
    template_name = 'index.html'

    def post(self, request, **kwargs):
        fs = FileSystemStorage()
        app_path = os.path.join(BASE_DIR, 'prediction')
        model_path = os.path.join(app_path, 'ai_model')
        # read ai model and its weight
        model = os.path.join(model_path, 'model.json')
        weights = os.path.join(model_path, 'weights_model.h5')
        K.reset_uids()
        with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
            with open(model, 'r') as f:
                model = model_from_json(f.read())
                model.load_weights(weights)
        myfile = request.FILES.getlist('myfile')
        if len(myfile) == 1:
            myfile = myfile[0]
            saved_file = fs.save(myfile.name, myfile)
            media_path = os.path.join(BASE_DIR, 'media')
            file_path = os.path.join(media_path, saved_file)
            img = image.load_img(file_path, target_size=(299, 299))
            img = image.img_to_array(img)
            img /= 255
            img = np.expand_dims(img, axis=0)
            # predicting image from ai model
            result = model.predict(img)
            number_of_leaf = result.flatten()[0]
            try:
                created_data_obj = cloudinary.uploader.upload(
                    file_path,
                    folder="my_folder/leaf_images/",
                    public_id="{}{}".format(myfile.name.split('.')[0],
                                            (str(round(time.time())))[:3]),
                    overwrite=True,
                    resource_type="raw"
                )
                secure_url = created_data_obj.get('secure_url')
            except:
                return HttpResponse("<h3> Sorry we can't process this document due to file size max_value exceed </h3>")
            uploaded_img_url = secure_url
            if request.user.is_authenticated:
                UserHistory.objects.create(
                    related_user=request.user,
                    number_of_leaf=number_of_leaf,
                    uploaded_img_url=uploaded_img_url,
                )
            os.remove(file_path)
            predicted_details = {
                'img_url': uploaded_img_url,
                'numebr_of_leaf': number_of_leaf,
                'isPrediction': True,
                'isMultiple': False,
            }
            messages.success(request, 'Your one image predicted successfully !!!')
            return super(TemplateView, self).render_to_response(predicted_details)
        elif len(myfile) > 1:
            predicted_images_detail = []
            for this_file in myfile:
                saved_file = fs.save(this_file.name, this_file)
                media_path = os.path.join(BASE_DIR, 'media')
                file_path = os.path.join(media_path, saved_file)
                img = image.load_img(file_path, target_size=(299, 299))
                img = image.img_to_array(img)
                img /= 255
                img = np.expand_dims(img, axis=0)
                # predicting image from ai model
                result = model.predict(img)
                number_of_leaf = result.flatten()[0]
                try:
                    created_data_obj = cloudinary.uploader.upload(
                        file_path,
                        folder="my_folder/leaf_images/",
                        public_id="{}{}".format(this_file.name.split('.')[0],
                                                (str(round(time.time())))[:3]),
                        overwrite=True,
                        resource_type="raw"
                    )
                    secure_url = created_data_obj.get('secure_url')
                except:
                    return HttpResponse("<h3> Sorry we can't process this document due to file size max_value exceed </h3>")
                uploaded_img_url = secure_url
                UserHistory.objects.create(
                    related_user=request.user,
                    number_of_leaf=number_of_leaf,
                    uploaded_img_url=uploaded_img_url,
                )
                os.remove(file_path)
                predicted_images_detail.append({
                    'img_url': uploaded_img_url,
                    'numebr_of_leaf': number_of_leaf
                })
            predicted_details = {
                'predicted_images': predicted_images_detail,
                'isPrediction': True,
                'isMultiple': True,
            }
            messages.success(request,
                             'Your {} images processed successfully !!!'.format(
                                 len(predicted_images_detail))
                             )
            return super(TemplateView, self).render_to_response(predicted_details)
        else:
            return HttpResponse("<h3> Sorry we can't process this document due to Form handling went wrong</h3>")


class SignUpFormView(SuccessMessageMixin, CreateView):
    """
    handle signup request
    """
    form_class = UserCreationForm
    success_message = "You account created successfully !!!"
    success_url = reverse_lazy('user_app:login')
    template_name = 'signup.html'


class LoginFormView(SuccessMessageMixin, LoginView):
    """
    class for authenticating user for login
    """
    success_message = "You were successfully logged IN !!!"
    template_name = 'login.html'

    def get_redirect_url(self):
        redirect_to = reverse_lazy('user_app:home')
        return redirect_to


class LogoutView(RedirectView):
    """class for logout """
    url = reverse_lazy('user_app:login')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You were successfully logged OUT !!!")
        return super(LogoutView, self).get(request, *args, **kwargs)


class HistoryPageView(LoginRequiredMixin, ListView):
    """
    class for handling history w.r.t requested user
    """
    model = UserHistory
    template_name = 'history.html'
    context_object_name = 'history_data'

    def get_queryset(self):
        new_context = json.dumps(list(UserHistory.objects.filter(
                                                    related_user=self.request.user.pk
        ).values()), cls=DjangoJSONEncoder)
        return new_context