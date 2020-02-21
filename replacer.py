import os
import shutil

#########################################

# Template string formatters

nl = '\n'
tab = '\t'

#########################################

# User Input

# Ask the user to input the name of their default project
project_name = input("Enter your project's name: ")

# Ask the user to input the name of their default app
app_name = input("Enter your app's name: ")

# # Ask the user to input the number of models they'll want to create
models_input = input('Enter the total number of models you wish to create: ')

# # Convert the number the user inputted (a string) to an INT for looping purposes
models_number = int(models_input)

#########################################

# Functions
def rename_folder(old_folder_name, replaced_name):
    for entry in os.scandir('./'):
        if entry.name.startswith(old_folder_name):
            os.rename(os.path.join('./', entry.name), os.path.join('./', entry.name.replace(old_folder_name, replaced_name.lower())))

def scan_files_and_replace(folder_name, old_file_name, replaced_file_name):
    for entry in os.scandir(f'./{folder_name}'):
        if entry.name.endswith('.py'):
            with open(entry) as file:
                s = file.read()
            replaced = s.replace(old_file_name, replaced_file_name)
            if entry.name.endswith('.py'):
                with open(entry, 'w') as f:
                    f.write(replaced)

#########################################

# PROJECT

# Replace the template project name with the user-defined name in the manage.py file
with open('./manage.py', 'r') as manager:
    manage = manager.read()
    manage = manage.replace('django_template_project', project_name)
with open('./manage.py', 'w') as manager:
    manager.write(manage)

# Scan the current directory's folders for a 'django_template_project' folder.  Replace the name with the user's Project Name input.
rename_folder('django_template_project', project_name)

# Scan the files within the app folder and replace "django_template_project" with the user's Project Name input.
scan_files_and_replace(project_name, 'django_template_project', project_name)

#########################################

# APP

# Change the app name in the {project_name}/settings.py file
with open(f'./{project_name}/settings.py', 'r') as settings_list:
    manage = settings_list.read()
    manage = manage.replace('django_template_app', app_name)
with open(f'./{project_name}/settings.py', 'w') as settings_list:
    settings_list.write(manage)

# Scan the current directory's folders for a 'django_template_app' folder.  Replace the name with the user's App Name input.
rename_folder('django_template_app', app_name)

# Scan the files within the Projects folder and replace "django_template_app" with the user's App Name input.
scan_files_and_replace(project_name, 'django_template_app', app_name)

# Scan the files within the App folder and replaced "django_template_app" with the user's App Name input.
scan_files_and_replace(app_name, 'django_template_app', app_name)

#########################################

# MODEL

os.mkdir(f'./{app_name}/templates/{app_name}')

for x in range(models_number):
    model_name = input('Enter the name for model ' + str(x + 1) + ': ')
    with open(f'./{app_name}/models.py', 'a+') as modelFile:
        modelFile.write(f'{nl}class {model_name}(models.Model):{nl}{tab}id = models.AutoField(primary_key=True){nl}{tab}{model_name.lower()}_name = models.CharField(max_length = 30)')
    with open(f'./{app_name}/views.py', 'a+') as viewFile:
        viewFile.write(f'{nl}{nl}class {model_name}ListView(ListView):{nl}{tab}model={model_name}')
        viewFile.write(f'{nl}{nl}class {model_name}DetailView(DetailView):{nl}{tab}model={model_name}{nl}{tab}template_name=\'{app_name}/{model_name.lower()}_detail.html\'')
        viewFile.write(f'{nl}{nl}class {model_name}CreateView(CreateView):{nl}{tab}model={model_name}{nl}{tab}template_name=\'{app_name}/{model_name.lower()}_add.html\'{nl}{tab}fields=\'__all__\'{nl}{tab}success_url=reverse_lazy(\'' + model_name.lower() + '-list\')')
        viewFile.write(f'{nl}{nl}class {model_name}UpdateView(UpdateView):{nl}{tab}model={model_name}{nl}{tab}template_name=\'{app_name}/{model_name.lower()}_edit.html\'{nl}{tab}fields=\'__all__\'{nl}{tab}success_url=reverse_lazy(\'' + model_name.lower() + '-list\')')
        viewFile.write(f'{nl}{nl}class {model_name}DeleteView(DeleteView):{nl}{tab}model={model_name}{nl}{tab}template_name=\'{app_name}/{model_name.lower()}_delete.html\'{nl}{tab}success_url=reverse_lazy(\'{model_name.lower()}-list\')')
    with open(f'./{app_name}/urls.py', 'a') as urls:
        urls.seek(urls.tell() - 1, os.SEEK_SET)
        urls.truncate()
        urls.write(f'{nl}{tab}path(\'{model_name.lower()}/\', {model_name}ListView.as_view(), name=\'{model_name.lower()}-list\'),')
        urls.write(f'{nl}{tab}path(\'{model_name.lower()}/<int:pk>/\', {model_name}DetailView.as_view(), name=\'{model_name.lower()}-detail\'),')
        urls.write(f'{nl}{tab}path(\'{model_name.lower()}/new/\', {model_name}CreateView.as_view(), name=\'{model_name.lower()}-create\'),')
        urls.write(f'{nl}{tab}path(\'{model_name.lower()}/edit/<int:pk>/\', {model_name}UpdateView.as_view(), name=\'{model_name.lower()}-edit\'),')
        urls.write(f'{nl}{tab}path(\'{model_name.lower()}/delete/<int:pk>/\', {model_name}DeleteView.as_view(), name=\'{model_name.lower()}-delete\'),{nl}')
        urls.write(']')
    with open(f'./{app_name}/forms.py', 'a') as forms:
        forms.write(f'{nl}class {model_name}Form(ModelForm):{nl}{tab}class Meta:{nl}{tab}{tab}model = {model_name}{nl}{tab}{tab}exclude = []{nl}{tab}{tab}fields = \'__all__\'{nl}')
    with open(f'./{app_name}/admin.py', 'a') as adminRegistry:
        adminRegistry.write(f'{nl}admin.site.register({model_name})')
    shutil.copyfile(f'./{app_name}/templates/index.html', f'./{app_name}/templates/{app_name}/{model_name}_list.html')
    shutil.copyfile(f'./{app_name}/templates/newmodel_add.html', f'./{app_name}/templates/{app_name}/{model_name}_add.html')
    shutil.copyfile(f'./{app_name}/templates/newmodel_delete.html', f'./{app_name}/templates/{app_name}/{model_name}_delete.html')
    shutil.copyfile(f'./{app_name}/templates/newmodel_detail.html', f'./{app_name}/templates/{app_name}/{model_name}_detail.html')
    shutil.copyfile(f'./{app_name}/templates/newmodel_edit.html', f'./{app_name}/templates/{app_name}/{model_name}_edit.html')
    for entry in os.scandir(f'./{app_name}/templates/{app_name}'):
        with open(entry, 'r') as current:
            read_entry = current.read()
            replace_text = read_entry.replace('newmodel', model_name.lower()).replace('ModelTitle', model_name).replace('ProjectTitle', f'{project_name} - {model_name}').replace('template_name', f'{model_name.lower()}_name')
        with open(entry, 'w') as current:
            current.write(replace_text)

os.system('python manage.py makemigrations')
os.system('python manage.py migrate')